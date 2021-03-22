from django.db.models import *


class Article(Model):
    title_main = CharField(max_length=70, null=False, blank=False)
    preface_main = TextField(max_length=500, null=True, blank=True)
    title_midmost = CharField(max_length=70, null=True, blank=True)
    preface_midmost = TextField(max_length=500, null=True, blank=True)
    text = TextField(max_length=3000, null=False, blank=False)

    def __str__(self):
        return self.title_main
