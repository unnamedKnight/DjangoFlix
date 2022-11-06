from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import render

from .models import Category
from playlists.models import Playlist

# Create your views here.


class CategoryListView(ListView):
    queryset = (
        Category.objects.all()
        .filter(active=True)
        .annotate(pl_count=Count("playlist"))
        .filter(pl_count__gt=0)
    )
    template_name = "categories/category_list_view.html"

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset


class CategoryDetailView(ListView):
    """
    Another list view for Playlist
    """

    queryset = Category.objects.filter(active=True)
    template_name = "categories/category_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("pk")
        try:
            obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist as e:
            raise Http404 from e
        if obj is not None:
            context["object"] = obj
            context["title"] = obj.title

        return context

    def get_queryset(self):
        # playlist = super().get_queryset()
        # we can skip the line above
        category_id = self.kwargs.get("pk")
        return Playlist.objects.filter(category__id=category_id).movie_or_show()
        # queryset = Category.objects.get(id=category_id).playlist_set.all()
        # queryset = obj.playlist_set.all()

