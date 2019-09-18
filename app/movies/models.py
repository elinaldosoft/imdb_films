from django.db import models
from django.utils.translation import ugettext_lazy as _

class Film(models.Model):
    tconst = models.IntegerField(unique=True, editable=False, db_index=True)
    title_type = models.CharField(max_length=50, null=True, blank=True)
    primary_title = models.CharField(max_length=500, null=True, blank=True)
    original_title = models.CharField(max_length=500, null=True, blank=True)
    is_adult = models.BooleanField(default=False)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=250)
    cache_average_rating = models.IntegerField(default=0)
    cache_num_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.primary_title

    def save(self, *args, **kwargs):
        self.tconst = tconst.replace('tt', '')
        self.start_year = None if self.start_year == '\\N' else self.start_year
        self.end_year = None if self.end_year == '\\N' else self.end_year
        self.runtime_minutes = None if self.runtime_minutes == '\\N' else self.runtime_minutes
        super(Film, self).save(*args, **kwargs)

    # class Meta:
    #     ordering = ['-version',]
    # https://stackoverflow.com/questions/16560055/django-admin-sorting-list-filter