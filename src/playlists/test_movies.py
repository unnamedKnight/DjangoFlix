from django.test import TestCase
from django.utils import timezone

from .models import MovieProxy, Playlist
from videos.models import Video


class MovieProxyTestCase(TestCase):
    def create_videos(self):
        video_a = Video.objects.create(title="My title", video_id="abc123")
        video_b = Video.objects.create(title="My title", video_id="abc1233")
        video_c = Video.objects.create(title="My title", video_id="abc1234")
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        self.video_qs = Video.objects.all()

    def setUp(self):
        self.create_videos()
        self.movie_a = MovieProxy.objects.create(
            title="This is my title", video=self.video_a
        )
        self.movie_b = MovieProxy.objects.create(
            title="This is my title2",
            state=Playlist.PublishStateOptions.PUBLISH,
            video=self.video_a,
        )
        movie_b = self.movie_b
        movie_b.videos.set(self.video_qs)
        movie_b.save()

    # def test_slug_field(self):
    #     title = self.obj_a.title
    #     test_slug = slugify(title)
    #     self.assertEqual(test_slug, self.obj_a.slug)

    def test_movie_video(self):
        self.assertEqual(self.movie_a.video, self.video_a)

    def test_movie_clip_items(self):
        count = self.movie_b.videos.all().count()
        self.assertEqual(count, 3)

    def test_valid_title(self):
        title = "This is my title"
        qs = MovieProxy.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_draft_case(self):
        qs = MovieProxy.objects.filter(state=Playlist.PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    # def test_draft_case1(self):
    #     obj = Playlist.objects.filter(state=Playlist.PublishStateOptions.DRAFT).first()
    #     self.assertFalse(obj.is_published)
    #     # self.assertFalse(self.obj_a.is_published)

    def test_publish_manager(self):
        published_qs = MovieProxy.objects.all().published()
        published_qs_2 = MovieProxy.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())
