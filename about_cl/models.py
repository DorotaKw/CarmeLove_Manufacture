from django.db.models import *
from django.template.defaultfilters import slugify
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


def my_slugify_function(content):
    return content.replace('_', '-').lower()


class Article(Model):
    title_main = CharField(max_length=70, null=False, blank=False)
    preface_main = TextField(max_length=500, null=True, blank=True)
    title_midmost = CharField(max_length=70, null=True, blank=True)
    preface_midmost = TextField(max_length=500, null=True, blank=True)
    text = TextField(max_length=3000, null=False, blank=False)
    slug = SlugField(null=False, unique=True)
    # slug = AutoSlugField(populate_from='title_main',
    #                      slugify_function=my_slugify_function,
    #                      editable=True)

    def __str__(self):
        return self.title_main

    @property
    def get_absolute_url(self):
        return reverse('about_cl:about_carmelove', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_main)
        return super().save(*args, **kwargs)

