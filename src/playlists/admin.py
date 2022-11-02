from django.contrib import admin
from .models import Playlist, PlaylistItem


# Register your models here.
class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    # extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]
    fields = [
        'title',
        'description',
        'slug',
        'state',
        'active'
    ]

    class Meta:
        model = Playlist

    # def get_queryset(self, request):
    #     return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)


admin.site.register(Playlist, PlaylistAdmin)
