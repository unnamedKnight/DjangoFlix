from django.shortcuts import render
from django.views import View
from playlists.models import Playlist
from django.http import Http404
from django.db.models import Count
from django.views.generic import ListView


from .models import TaggedItem

# Create your views here.


class TaggedItemListView(View):
    def get(self, request):
        tag_list = TaggedItem.objects.unique_list()
        context = {
            "tag_list": tag_list,
        }

        return render(request, "tags/tags_list.html", context)


class TaggedItemDetailView(ListView):
    """
    Another list view for Playlist
    """
    template_name = 'tags/tag_detail.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = f"{self.kwargs.get('tag')}".title()
        return context
    
    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return Playlist.objects.filter(tags__tag__contains=tag).movie_or_show()
