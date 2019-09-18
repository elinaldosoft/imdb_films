from django.contrib import admin
from .models import Film


@admin.register(Film)
class AdminFilm(admin.ModelAdmin):
    # list_filter = ('start_year', )
    search_fields = ['content_search']
    list_display = ['primary_title', 'start_year', 'cache_average_rating', 'cache_num_votes']
    readonly_fields = ['tconst']
    list_per_page = 20