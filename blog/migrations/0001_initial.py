# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-01 02:40
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField()),
                ('focus', models.CharField(blank=True, max_length=55, null=True)),
                ('content', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('twit', models.BooleanField(default=False)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'media/posts/img'), upload_to=b'')),
                ('video', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'media/posts/vid'), upload_to=b'')),
                ('sound_cloud', models.CharField(blank=True, max_length=25, null=True)),
                ('video_type', models.CharField(blank=True, max_length=4, null=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
    ]