from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy


# Create your views here.


class PlaylistMixin:
    # title = None
    template_name = "playlists/playlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['movies'] = MovieProxy.objects.all()
        if self.title is not None:
            context["title"] = self.title
        return context

    # def get_queryset(self):
    #     # print(super().get_queryset().published())
    #     return super().get_queryset().published()


class SearchView(PlaylistMixin, ListView):
    title = "Search"
    template_name = "playlists/search.html"
    
    
    def get_context_data(self):
        context = super().get_context_data()
        query = self.request.GET.get("q")
        if query is not None:
            context["title"] = f"Searched for {query}"
        else:
            context["title"] = "Perform a search"
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")  # request.GET = {}
        qs = Playlist.objects.all().movie_or_show().search(query=query)
        print(qs)
        return qs


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    template_name = "playlists/featured_playlist.html"
    queryset = Playlist.objects.featured_playlists()
    title = "Featured Playlist"


class FeaturedPlaylistDetailView(PlaylistMixin, DetailView):
    template_name = "playlists/playlist_detail.html"
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
    title = "Movie Details"
    template_name = "playlists/movie_detail.html"


class TVShowListView(PlaylistMixin, ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV-Show"


# class TVShowView(PlaylistMixin, DetailView):
#     model = TVShowProxy
#     title = 'TVShow Details'
#     template_name = 'playlists/movie_detail.html'


class TVShowDetailView(PlaylistMixin, DetailView):
    model = TVShowProxy
    title = "TVShow Details"
    template_name = "playlists/tvshow_detail.html"


class TVShowSeasonDetailView(PlaylistMixin, DetailView):

    # when using complex url like
    # tv-shows-detail/<int:showPk>/season/<int:pk>
    # where 2 primary keys are used  we dont need to get the primary key through kwargs
    # if using pk as the identifier of primary key
    # here in the above example of URL the first primary key will be ignored by django
    # and django will return the object based on the last primary key
    template_name = "playlists/season_detail.html"
    queryset = TVShowSeasonProxy.objects.all()
    title = "TVShow Season Details"

    # def get_object(self):
    #     request = self.request
    #     kwargs = self.kwargs

    #     parent_pk = kwargs.get('showPk')
    #    # when using primary key name other than pk
    #    # we have to get that pk through kwargs
    #     season_pk = kwargs.get('seasonPk')
    #     try:
    #         query_object = self.get_queryset().get(parent__id=parent_pk, id=season_pk)
    #     except TVShowSeasonProxy.DoesNotExist:
    #         raise Http404
    #
    #     return query_object
