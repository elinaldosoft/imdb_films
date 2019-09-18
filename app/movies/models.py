from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.translation import ugettext_lazy as _

class Film(models.Model):
    tconst = models.CharField(max_length=50, unique=True, editable=False, db_index=True)
    title_type = models.CharField(max_length=50, null=True, blank=True)
    primary_title = models.CharField(max_length=500, null=True, blank=True)
    original_title = models.CharField(max_length=500, null=True, blank=True)
    is_adult = models.BooleanField(default=False)
    start_year = models.CharField(max_length=250, null=True, blank=True)
    end_year = models.CharField(max_length=250, null=True, blank=True)
    runtime_minutes = models.CharField(max_length=250, null=True, blank=True)
    genres = models.CharField(max_length=250, null=True, blank=True)
    cache_average_rating = models.IntegerField(default=0)
    cache_num_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content_search = SearchVectorField(null=True)

    class Meta:
        db_table = 'films'
        indexes = [GinIndex(fields=["content_search"])]

    def __str__(self):
        return self.primary_title