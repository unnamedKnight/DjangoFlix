from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy


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

    # def get_queryset(self):
    #     # print(super().get_queryset().published())
    #     return super().get_queryset().published()


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    # template_name = 'playlists/featured_list.html'
    queryset = Playlist.objects.featured_playlists()
    title = "Featured"


class FeaturedPlaylistDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/playlist_detail.html'
    title = "Detail"
    queryset = Playlist.objects.all()

    # def get_object(self, queryset=None):
    #     request = self.request
    #     kwargs = self.kwargs
    #     return self.get_queryset().filter(**kwargs).first()


class MovieListView(PlaylistMixin, ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(MovieListView, self).get_context_data(*args, **kwargs)
    #     # context['movies'] = MovieProxy.objects.all()
    #     context['title'] = self.title
    #     return context


class MovieDetailView(PlaylistMixin, DetailView):
    model = MovieProxy
    title = 'Movie Details'
    template_name = 'playlists/movie_detail.html'


class TVShowListView(PlaylistMixin, ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV-Show"


# class TVShowView(PlaylistMixin, DetailView):
#     model = TVShowProxy
#     title = 'TVShow Details'
#     template_name = 'playlists/movie_detail.html'


class TVShowDetailView(PlaylistMixin, DetailView):
    model = TVShowProxy
    title = 'TVShow Details'
    template_name = 'playlists/tvshow_detail.html'


class TVShowSeasonDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()
    title = "TVShow Season Details"

    def get_object(self):
        request = self.request
        kwargs = self.kwargs
        parent_pk = kwargs.get('showPk')
        season_pk = kwargs.get('seasonPk')
        qs = self.get_queryset().filter(parent__id=parent_pk, id=season_pk)
        if not qs.count() == 1:
            raise Exception('Not Found')
        return qs.first()
