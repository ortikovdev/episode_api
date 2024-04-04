from django.contrib import admin

# Register your models here.

from .models import Episode, EpisodeComment, EpisodeLike


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'get_image')
    readonly_fields = ('slug', 'modified_date', 'created_date')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    date_hierarchy = 'created_date'
    filter_horizontal = ('tags', )
    autocomplete_fields = ('author',)
    save_on_top = True


@admin.register(EpisodeComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'episode', 'author', 'top_level_comment_id', 'parent')
    search_fields = ('name', '')
    readonly_fields = ('created_date', )
    autocomplete_fields = ('episode', )


@admin.register(EpisodeLike)
class EpisodeLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'episode', 'author', )
    autocomplete_fields = ('episode', 'author', )
    search_fields = ('episode', )





