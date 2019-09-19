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
from config.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Import movies and ratings'

    def add_arguments(self, parser):
        parser.add_argument('import', type=str, help='import films')
        parser.add_argument('--films', type=str, help='import_ratings')
        parser.add_argument('--ratings', type=str, help='import_ratings')

    def import_ratings(self):
        url = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
        chunks = pd.read_table(url, compression='gzip', sep='\t', encoding='utf-8', chunksize=50000, iterator=True, na_filter=False)
        sql = "UPDATE public.films SET cache_average_rating = %s, cache_num_votes = %s WHERE tconst = %s"
        for df in chunks:
            data = []
            for item in df.values:
                item = list(map(lambda x: str(x), item))
                data.append([item[1], item[2], item[0]])
            with closing(connection.cursor()) as cursor:
                cursor.executemany(sql, data)
                data = []
                self.stdout.write(self.style.SUCCESS('Commit 50k'))

    def import_films(self):
        url = 'https://datasets.imdbws.com/title.basics.tsv.gz'
        chunks = pd.read_table(url, compression='gzip', sep='\t', encoding='utf-8', chunksize=50000, iterator=True, na_filter=False)
        for df in chunks:
            stream = StringIO()
            writer = csv.writer(stream, delimiter='\t')
            for item in df.values:
                if "\t" in str(item[2]):
                    item = list(item)
                    item = item[0:2] + item[2].split('\t') + item[3:8] #fix bad format in file
                writer.writerow(list(map(lambda x: str(x), item)))
            stream.seek(0)
            with closing(connection.cursor()) as cursor:
                self.stdout.write(self.style.SUCCESS('Commit 50k'))
                cursor.copy_from(
                    file=stream,
                    table='films',
                    sep='\t',
                    columns=("tconst", "title_type", "primary_title", "original_title", "is_adult", "start_year", "end_year", "runtime_minutes", "genres")
                )

    def handle(self, *args, **options):
        if 'films' == options['import']:
            self.stdout.write(self.style.NOTICE('Movie import starting'))
            self.import_films()
            self.stdout.write(self.style.NOTICE('Movie import finished'))
        elif 'ratings' == options['import']:
            self.stdout.write(self.style.NOTICE('Rating import starting'))
            self.import_ratings()
            self.stdout.write(self.style.NOTICE('Rating import starting'))