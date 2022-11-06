from django.urls import path

from . import views

urlpatterns = [
    path("", views.CategoryListView.as_view(), name="category_view"),
    path("detail/<int:pk>", views.CategoryDetailView.as_view(), name="category_detail"),
]
