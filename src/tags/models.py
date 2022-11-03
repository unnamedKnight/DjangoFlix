from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class TaggedItem(models.Model):
    tag = models.SlugField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # def get_related_object(self):
    #     model_class = self.content_type.model_class()
    #     return model_class.objects.get(id=self.object_id)


