from django.db import models
from django.utils.translation import ugettext_lazy as _

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Film(TimeStamped):
    tconst = models.IntegerField(unique=True, editable=False, db_index=True)
    title_type = models.CharField(max_length=50, null=True, blank=True)
    primary_title = models.CharField(max_length=250, null=True, blank=True)
    original_title = models.CharField(max_length=250, null=True, blank=True)
    is_adult = models.BooleanField(default=False)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=250)
    cache_average_rating = models.IntegerField(default=0)
    cache_num_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.primary_title