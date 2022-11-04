from django.urls import path

from . import views

urlpatterns = [
        path('', views.FeaturedPlaylistListView.as_view(), name='home'),
        path('movies', views.MovieListView.as_view(), name='movies'),
        path('tv-shows', views.TVShowListView.as_view(), name='tv_shows'),
]
