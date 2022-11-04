from django.shortcuts import render
from django.views.generic import ListView

from .models import Playlist, MovieProxy, TVShowProxy


# Create your views here.

class PlaylistMixin():
    title = None
    template_name = 'playlists/playlist.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['movies'] = MovieProxy.objects.all()
        if self.title is not None:
            context['title'] = self.title
        return context


class MovieListView(PlaylistMixin, ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(MovieListView, self).get_context_data(*args, **kwargs)
    #     # context['movies'] = MovieProxy.objects.all()
    #     context['title'] = self.title
    #     return context


class TVShowListView(PlaylistMixin, ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV-Show"


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    # template_name = 'playlists/featured_list.html'
    queryset = Playlist.objects.featured_playlists()
    title = "Featured"
