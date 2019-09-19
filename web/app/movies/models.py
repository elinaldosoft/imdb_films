from django.db import models
from django.utils.translation import ugettext_lazy as _

class Film(models.Model):
    tconst = models.IntegerField(unique=True, editable=False, db_index=True)
    title_type = models.CharField(max_length=50, null=True, blank=True)
    primary_title = models.CharField(max_length=500, null=True, blank=True)
    original_title = models.CharField(max_length=500, null=True, blank=True)
    is_adult = models.BooleanField(default=False)
    start_year = models.CharField(max_length=250, null=True, blank=True)
    end_year = models.CharField(max_length=250, null=True, blank=True)
    runtime_minutes = models.CharField(max_length=250, null=True, blank=True)
    genres = models.CharField(max_length=250, null=True, blank=True)
    cache_average_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cache_num_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'films'
        ordering = ['-cache_num_votes', '-cache_average_rating',]

    def __str__(self):
        return self.primary_title

class Rating(models.Model):
    tconst = models.IntegerField(unique=True, editable=False, db_index=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    num_votes = models.IntegerField(default=0)
    class Meta:
        db_table = 'ratings'
