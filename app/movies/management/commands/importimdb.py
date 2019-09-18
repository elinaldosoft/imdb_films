import os
import subprocess
import time
import re
from io import StringIO
import csv
from contextlib import closing
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from app.movies.models import Film
from config.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('import', type=str, help='import films')
        parser.add_argument('--films', type=str, help='import_ratings')
        parser.add_argument('--ratings', type=str, help='import_ratings')

    def import_ratings(self):
        url = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
        chunks = pd.read_table(url, compression='gzip', sep='\t', encoding='utf-8', chunksize=50000, iterator=True, na_filter=False)
        for df in chunks:
            for item in df.values:
                
                # UPDATE "public"."films" SET "cache_average_rating" = '1', "cache_num_votes" = '2' WHERE "tconst" = '39';
                print(item)

    def import_films(self):
        path = os.path.join(BASE_DIR, 'data', 'title.basics.tsv.gz')
        chunks = pd.read_table(path, compression='gzip', sep='\t', encoding='utf-8', chunksize=50000, iterator=True, na_filter=False)
        for df in chunks:
            stream = StringIO()
            writer = csv.writer(stream, delimiter='\t')
            for item in df.values:
                if "\t" in str(item[2]):
                    item = list(item)
                    item = item[0:2] + item[2].split('\t') + item[3:8]
                writer.writerow(list(map(lambda x: str(x), item)))
            stream.seek(0)
            with closing(connection.cursor()) as cursor:
                cursor.copy_from(
                    file=stream,
                    table='films',
                    sep='\t',
                    columns=("tconst", "title_type", "primary_title", "original_title", "is_adult", "start_year", "end_year", "runtime_minutes", "genres")
                )
        connection.close()

    def handle(self, *args, **options):
        if 'films' == options['import']:
            self.import_films()
        elif 'ratings' == options['import']:
            self.import_ratings()
        
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))