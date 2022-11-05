from django.contrib import admin
from tags.admin import TaggedItemInline
from .models import MovieProxy, TVShowProxy, TVShowSeasonProxy, Playlist, PlaylistItem, PlaylistRelated


# Register your models here.


class MovieProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["title"]
    fields = ["title", "state", "category", "video"]

    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()


admin.site.register(MovieProxy, MovieProxyAdmin)


class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    # extra = 0


class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline, SeasonEpisodeInline]
    list_display = ["title", "parent"]

    class Meta:
        model = TVShowSeasonProxy

    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()


admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)


class TVShowSeasonProxyInline(admin.TabularInline):
    fields = ["title", "state", "video"]
    model = TVShowSeasonProxy
    # extra = 0


class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline, TVShowSeasonProxyInline]
    list_display = ["title"]
    fields = ["order", "title", "category", "state"]

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return TVShowProxy.objects.all()


admin.site.register(TVShowProxy, TVShowProxyAdmin)


class PlaylistRelatedInline(admin.TabularInline):
    model = PlaylistRelated
    fk_name = 'playlist'
    extra = 0


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    # extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistRelatedInline, TaggedItemInline, PlaylistItemInline]
    fields = ["title", "description", "category", "state", "video"]

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)


admin.site.register(Playlist, PlaylistAdmin)
