from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaggedItemListView.as_view(), name='tags_list_view'),
    path('tag-detail/<slug:tag>', views.TaggedItemDetailView.as_view(), name='tag_detail_view')
]