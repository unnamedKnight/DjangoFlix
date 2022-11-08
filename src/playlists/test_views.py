from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from .models import Playlist, TVShowProxy, MovieProxy


class PlaylistViewTestCase(TestCase):
    # fixtures = [settings.BASE_DIR / 'proj.json']
    fixtures = ["projects"]

    def test_movie_count(self):
        qs = MovieProxy.objects.all()
        self.assertEqual(qs.count(), 3)

    def test_show_count(self):
        qs = TVShowProxy.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_movie_detail_view(self):
        movie = MovieProxy.objects.all().published().first()
        print(movie)
        # pk = show.id
        url = movie.get_absolute_url()
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{movie.title}")  # look into the
        # response html --> show.title
        context = response.context
        obj = context["object"]
        self.assertEqual(movie.id, obj.id)

    def test_show_detail_view(self):
        show = TVShowProxy.objects.all().published().first()
        pk = show.id
        url = show.get_absolute_url()
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{show.title}")  # look into the
        # response html --> show.title
        context = response.context
        obj = context["object"]
        self.assertEqual(show.id, obj.id)

    def test_movie_list_view(self):
        movie = MovieProxy.objects.all().published()
        url = "/movies"
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = response.context
        obj_list = context["object_list"]
        self.assertQuerysetEqual(
            movie.order_by("-timestamp"), obj_list.order_by("-timestamp")
        )
    
    def test_show_list_view(self):
        shows = TVShowProxy.objects.all().published()
        url = "/tv-shows"
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = response.context
        obj_list = context["object_list"]
        self.assertQuerysetEqual(
            shows.order_by("-timestamp"), obj_list.order_by("-timestamp")
        )
    
    def test_search_results_view(self):
        query = "Action"
        response = self.client.get(f"/search/?q={query}")
        # print(f' thsi is response: {response}')
        ply_qs = Playlist.objects.all().movie_or_show().search(query=query)
        print(f"this is playlist-qs: {ply_qs}")
        self.assertEqual(response.status_code, 200)  # 200
        context = response.context
        r_qs = context["object_list"]
        self.assertQuerysetEqual(
            ply_qs.order_by("-timestamp"), r_qs.order_by("-timestamp")
        )
        self.assertContains(response, f"Searched for {query}")
