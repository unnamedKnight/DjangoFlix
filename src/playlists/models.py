from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, Max, Min, Q
from django.db.models.signals import pre_save
from django.utils import timezone

from videos.models import Video


# Create your models here.

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=Playlist.PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    # class PlaylistTypeChoices(models.TextChoices):
    #     MOVIE = "MOV", "Movie"
    #     SHOW = 'TVS', "TV Show"
    #     SEASON = 'SEA', "Season"
    #     PLAYLIST = 'PLY', "Playlist"

    class PublishStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'

    # parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    # order = models.IntegerField(default=1)
    title = models.CharField(max_length=220)
    # type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(Video, related_name='playlist_featured', blank=True, null=True,
                              on_delete=models.SET_NULL)  # one video per playlist
    videos = models.ManyToManyField(Video, related_name='playlist_item', blank=True, through='PlaylistItem')
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = PlaylistManager()

    @property
    def is_published(self):
        return self.active

    def __str__(self):
        return self.title


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == instance.PublishStateOptions.PUBLISH
    is_draft = instance.state == instance.PublishStateOptions.DRAFT
    if is_publish and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None


pre_save.connect(publish_state_pre_save, sender=Playlist)
