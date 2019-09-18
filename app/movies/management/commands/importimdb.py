import os
import subprocess
import time
import re
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from app.movies.models import Film
from config.settings import BASE_DIR

REGEX = r"^(tt[0-9]+)\s+([\w]+)\s+(.*)\s+(.*)\s+([0-1])\s+(\\N|[0-9]{4})\s+(\\N|[0-9]{4})\s+(\\N|[0-9]+)\s+(.*)$"

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('films', type=str, help='import films')

    # async def generate_sql(table: str, columns: list) -> str:
    # values = ", ".join(["$%s" % v for v in range(1, len(columns) + 1)])
    # columns = ", ".join([util.snake_case(c) for c in columns])
    # table = util.snake_case(table)
    # sql = f"INSERT INTO public.{table} ({columns}) VALUES ({values});"
    # return sql

    # def process_file(self, path_file):
    #     count = 0
    #     insert = []
    #     size = self.count_file_lines(path_file)
    #     self.stdout.write(self.style.NOTICE('Starting importing'))
    #     with open(path_file) as file:
    #         for f in file.readlines():
    #             count += 1
    #             f = re.search(REGEX, f)
    #             if f:
    #                 start_year = f.group(6)
    #                 end_year = f.group(7)
    #                 runtime_minutes = f.group(8)
    #                 if start_year == '\\N':
    #                     start_year = None
    #                 if end_year == '\\N':
    #                     end_year = None
    #                 if runtime_minutes == '\\N':
    #                      runtime_minutes = None
    #                 insert.append(Film(
    #                     tconst=f.group(1).replace('tt', ''),
    #                     title_type=f.group(2),
    #                     primary_title=f.group(3),
    #                     original_title=f.group(4),
    #                     is_adult=f.group(5),
    #                     start_year=start_year,
    #                     end_year=end_year,
    #                     runtime_minutes=runtime_minutes,
    #                     genres=f.group(9)
    #                 ))
    #             if count % 100000 == 0 or count == size:
    #                 per = round((100 * count) / size, 2)
    #                 Film.objects.bulk_create(insert)
    #                 self.stdout.write(self.style.SUCCESS(f"Receiving objects:  {per}% ({count}/{size})"))
    #                 insert = []
    #     self.stdout.write(self.style.NOTICE('Finished importing'))

    def generate_sql(self, table: str, columns: list) -> str:
        values = ["%s" for _ in range(1, 9)]
        values = ", ".join(values)
        columns = ", ".join([c for c in columns])
        sql = f"INSERT INTO public.{table} ({columns}) VALUES ({values});"
        return sql

    def import_films(self):
        path = os.path.join(BASE_DIR, 'data', 'title.basics.tsv.gz')
        from contextlib import closing
        from io import StringIO
        chunks = pd.read_table(path, compression='gzip', sep='\t', encoding='utf-8', chunksize=50000, iterator=True)
        for df in chunks:
            output = StringIO()
            # pd.read_table(path, compression='gzip', sep='\t', encoding='utf-8', header=None)
            df.values()
            output.seek(0)

            with closing(connection.cursor()) as cursor:
                cursor.copy_from(
                    file=output,
                    table='movies_film',
                    sep='\t',
                    columns=("tconst", "title_type", "primary_title", "original_title", "is_adult", "start_year", "genres")
                )
            connection.commit()
        # chunks = pd.read_table(path, compression='gzip', sep='\t', encoding='utf-8', chunksize=50000, iterator=True)
        # query = self.generate_sql("movies_film", ["tconst", "title_type", "primary_title", "original_title", "is_adult", "start_year", "genres", "cache_average_rating", "cache_num_votes", "created_at", "updated_at"])
        # for df in chunks:
        #     values = []
        #     for item in df.values:
        #         item[5] = 'NULL' if item[5] == '\\N' else item[5]
        #         item[6] = 'NULL' if item[6] == '\\N' else item[6]
        #         item[7] = 'NULL' if item[7] == '\\N' else item[7]
        #         values.append(list(map(lambda x: str(x), item)))
        #     cursor = connection.cursor()
        #     cursor.executemany(query, values, ())
            # print(data)
        #     Film.objects.bulk_create(insert)
        #print(insert)
        # chunks = os.path.join(BASE_DIR, 'data/chunks/')
        # pool = ThreadPoolExecutor(10)
        # future_results = []

        # for file in os.listdir(chunks):
        #     path = os.path.join(chunks, file)
        #     future_results.append(pool.submit(process_file, path))
        # wait(future_results)

    def handle(self, *args, **options):
        if 'films' in options:
            self.import_films()
        
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))