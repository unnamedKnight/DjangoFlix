from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from tags.models import TaggedItem


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=240)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = GenericRelation(TaggedItem, related_query_name='category')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.id})