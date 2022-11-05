from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone


# Create your models here.

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=Video.PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    class PublishStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'

    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)  # 'this-is-my-video'
    video_id = models.CharField(max_length=220, blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = VideoManager()

    def __str__(self):
        return self.title

    def get_video_id(self):

        # if not self.is_published:
        #     return None
        # return self.video_id
        #  # alternative of the above operations
        return self.id if self.is_published else None

    @property
    def is_published(self):
        if not self.active:
            return False
        state = self.state
        if state != Video.PublishStateOptions.PUBLISH:
            return False
        publish_timestamp = self.publish_timestamp
        if publish_timestamp is None:
            return False
        now = timezone.now()
        return publish_timestamp <= now
    # def get_playlist_ids(self):
    #     # self.<foreigned_obj>_set.all()
    #     return list(self.playlist_featured.all().values_list('id', flat=True))


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'


def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == instance.PublishStateOptions.PUBLISH
    is_draft = instance.state == instance.PublishStateOptions.DRAFT
    if is_publish and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None


pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(publish_state_pre_save, sender=VideoAllProxy)
pre_save.connect(publish_state_pre_save, sender=VideoPublishedProxy)
