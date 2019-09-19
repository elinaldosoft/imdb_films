from django.contrib import admin
from .models import Film


@admin.register(Film)
class AdminFilm(admin.ModelAdmin):
    # list_filter = ('start_year', )
    search_fields = ['primary_title']
    list_display = ['primary_title', 'start_year', 'rating', 'votes']
    readonly_fields = ['tconst']
    list_per_page = 20

    def rating(self, obj):
        return obj.cache_average_rating
    rating.short_description = 'Rating'

    def votes(self, obj):
        return obj.cache_num_votes
    votes.short_description = 'Votes'