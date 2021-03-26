# Generated by Django 3.1.6 on 2021-03-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_main', models.CharField(max_length=70)),
                ('preface_main', models.TextField(blank=True, max_length=500, null=True)),
                ('title_midmost', models.CharField(blank=True, max_length=70, null=True)),
                ('preface_midmost', models.TextField(blank=True, max_length=500, null=True)),
                ('text', models.TextField(max_length=3000)),
            ],
        ),
    ]