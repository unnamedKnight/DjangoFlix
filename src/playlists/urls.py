from django.urls import path

from . import views

urlpatterns = [
    path("", views.FeaturedPlaylistListView.as_view(), name="home"),
    path("media/<int:pk>", views.FeaturedPlaylistDetailView.as_view(), name="media_detail"),
    path("movie-detail/<int:pk>", views.MovieDetailView.as_view(), name="movie_detail"),
    path("movies", views.MovieListView.as_view(), name="movies"),
    path(
        "tv-shows-detail/<int:pk>",
        views.TVShowDetailView.as_view(),
        name="tv_show_detail",
    ),
    path(
        "tv-shows-detail/<int:showPk>/season/<int:pk>",
        views.TVShowSeasonDetailView.as_view(),
        name="tv_show_season_detail",
    ),
    path("tv-shows", views.TVShowListView.as_view(), name="tv_shows"),
]
