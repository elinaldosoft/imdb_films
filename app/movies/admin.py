from django.contrib import admin
from .models import Film


@admin.register(Film)
class AdminFilm(admin.ModelAdmin):
    search_fields = ['primary_title', 'original_title']
    list_display = ['primary_title', 'start_year', 'cache_average_rating', 'cache_num_votes']
