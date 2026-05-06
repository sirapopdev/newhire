from django.db import models
from oscar.models.fields import AutoSlugField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', editable=True, unique=True)

    def __str__(self):
        return self.name