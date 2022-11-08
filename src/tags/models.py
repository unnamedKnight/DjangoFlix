from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import pre_save


# Create your models here.


class TaggedItemManager(models.Manager):
    def unique_list(self):
        tags_set = set(self.get_queryset().values_list("tag", flat=True))
        # tags_list = sorted(list(tags_set))
        return sorted(list(tags_set))


class TaggedItem(models.Model):
    tag = models.SlugField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = TaggedItemManager()

    # def get_related_object(self):
    #     model_class = self.content_type.model_class()
    #     return model_class.objects.get(id=self.object_id)

    def __str__(self) -> str:
        return f'{self.tag} {self.id}'


def lowercase_tag_slug(sender, instance, *args, **kwargs):
    slug = instance.tag.lower()
    instance.tag = slug


pre_save.connect(lowercase_tag_slug, sender=TaggedItem)
