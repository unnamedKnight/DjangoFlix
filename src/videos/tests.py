from django.test import TestCase
from django.utils import timezone

from .models import Video


class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a = Video.objects.create(title='This is my title')
        self.obj_b = Video.objects.create(title='This is my title', state=Video.PublishStateOptions.PUBLISH,
                                          )

    # def test_slug_field(self):
    #     title = self.obj_a.title
    #     test_slug = slugify(title)
    #     self.assertEqual(test_slug, self.obj_a.slug)

    def test_valid_title(self):
        title = 'This is my title'
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=Video.PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_draft_case1(self):
        obj = Video.objects.filter(state=Video.PublishStateOptions.DRAFT).first()
        # self.assertFalse(obj.is_published)
        self.assertFalse(obj.is_published)

    def test_publish_case(self):
        qs = Video.objects.filter(state=Video.PublishStateOptions.PUBLISH).first()
        self.assertTrue(qs.is_published)

    def test_publish_case1(self):
        obj = Video.objects.filter(state=Video.PublishStateOptions.PUBLISH).first()
        self.assertTrue(obj.is_published)

    def test_publish_manager(self):
        published_qs = Video.objects.all().published()
        published_qs_2 = Video.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())
