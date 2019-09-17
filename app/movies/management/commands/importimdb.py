import os
import subprocess
import re
from django.core.management.base import BaseCommand, CommandError
from app.movies.models import Film
from config.settings import BASE_DIR

REGEX = r"^(tt[0-9]+)\s+([\w]+)\s+(.*)\s+(.*)\s+([0-1])\s+(\\N|[0-9]{4})\s+(\\N|[0-9]{4})\s+(\\N|[0-9]+)\s+(.*)$"

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)


    def count_file_lines(self, file_path):
        num = subprocess.check_output(['wc', '-l', file_path])
        num = num.split(' ')
        return int(num[0])

    def import_films(self):
        count = 0
        path = os.path.join(BASE_DIR, 'data', 'title.basics.tsv')
        insert = []
        size = self.count_file_lines(path)

        with open(path) as file:
            for f in file.readlines():
                count += 1
                f = re.search(REGEX, f)
                if f:
                    start_year = f.group(6)
                    end_year = f.group(7)
                    runtime_minutes = f.group(8)
                    if start_year == '\\N':
                        start_year = None
                    if end_year == '\\N':
                        end_year = None
                    if runtime_minutes == '\\N':
                         runtime_minutes = None
                    insert.append(Film(
                        tconst=f.group(1).replace('tt', ''),
                        title_type=f.group(2),
                        primary_title=f.group(3),
                        original_title=f.group(4),
                        is_adult=f.group(5),
                        start_year=start_year,
                        end_year=end_year,
                        runtime_minutes=runtime_minutes,
                        genres=f.group(9)
                    ))
                if count % 100000 == 0 or count == size:
                    Film.objects.bulk_create(insert)
                    insert = []
        self.stdout.write(self.style.SUCCESS('Finished importing'))

    def handle(self, *args, **options):
        pass
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))