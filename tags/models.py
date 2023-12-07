from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=255)


class TaggedItem(models.Model):
    # what tag is for what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # content type,id
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey()
