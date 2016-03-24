# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields
import versatileimagefield.fields
import django.core.files.storage
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bureau',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=35, choices=[(b'Patrol', b'Patrol'), (b'Investigations', b'Investigations'), (b'Administrative', b'Administrative')])),
                ('task', models.TextField()),
                ('address', models.CharField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.CharField(max_length=55, null=True, blank=True)),
                ('notes', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=75)),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('date', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('location', models.CharField(max_length=75, null=True, blank=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['-date', 'officer__name'],
                'verbose_name_plural': 'Complaints',
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('task', models.TextField()),
                ('address', models.CharField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.CharField(max_length=55, null=True, blank=True)),
                ('notes', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=55)),
                ('bureau', models.ForeignKey(blank=True, to='copwatch.Bureau', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=35)),
                ('image', versatileimagefield.fields.VersatileImageField(storage=django.core.files.storage.FileSystemStorage(location=b'media/cops/faces'), null=True, upload_to=b'', blank=True)),
                ('image_new', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True, max_length=125)),
                ('ht_feet', models.CharField(blank=True, max_length=5, null=True, choices=[(b'4', b'4'), (b'5', b'5'), (b'6', b'6'), (b'7', b'7')])),
                ('ht_inch', models.CharField(blank=True, max_length=5, null=True, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5'), (b'6', b'6'), (b'7', b'7'), (b'8', b'8'), (b'9', b'9'), (b'10', b'10'), (b'11', b'11')])),
                ('weight', models.SmallIntegerField(null=True, blank=True)),
                ('hair_color', models.CharField(blank=True, max_length=6, null=True, choices=[(b'Brown', b'Brown'), (b'Blonde', b'Blonde'), (b'Black', b'Black'), (b'Grey', b'Grey'), (b'Other', b'Other')])),
                ('eye_col', models.CharField(blank=True, max_length=5, null=True, choices=[(b'Brown', b'Brown'), (b'Green', b'Green'), (b'Blue', b'Blue'), (b'Other', b'Other')])),
                ('race', models.CharField(blank=True, max_length=7, null=True, choices=[(b'White', b'White'), (b'Latino', b'Latino'), (b'Black', b'Black'), (b'Asian', b'Asian'), (b'Mixed', b'Mixed')])),
                ('ethnicity', models.CharField(max_length=12, null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=25, null=True, choices=[(b'Married', b'Married'), (b'Single', b'Single'), (b'Divorced', b'Divorced')])),
                ('city_of_residence', models.CharField(max_length=55, null=True, blank=True)),
                ('phone', models.CharField(blank=True, max_length=b'10', null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{10}$', message=b"Phone number must be entered in the format: '1234567890'. Ten digits, include the area code.")])),
                ('email', models.CharField(max_length=55, null=True, blank=True)),
                ('alma_mater', models.CharField(max_length=25, null=True, blank=True)),
                ('salary', models.IntegerField(null=True, blank=True)),
                ('rank', models.CharField(blank=True, max_length=25, null=True, choices=[(b'Officer', b'Officer'), (b'Sergeant', b'Sergeant'), (b'Investigative Team Leader', b'Investigative Team Leader'), (b'Lieutenant', b'Lieutenant'), (b'Captain', b'Captain'), (b'Inspector', b'Inspector'), (b'Deputy Chief', b'Deputy Chief'), (b'Chief of Police', b'Chief of Police'), (b'Union Rep', b'Union Rep'), (b'Admin', b'Admin')])),
                ('badge', models.CharField(blank=True, max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{1,7}$', message=b"Badge number must be entered in the format: '1234567'.")])),
                ('years_emp_mps', models.SmallIntegerField(null=True, blank=True)),
                ('years_emp_law', models.SmallIntegerField(null=True, blank=True)),
                ('notes', models.TextField()),
            ],
            options={
                'ordering': ['precinct', 'rank', 'name'],
                'verbose_name_plural': 'Officers',
            },
        ),
        migrations.CreateModel(
            name='Precinct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precinct', models.CharField(max_length=10, choices=[(b'1st', b'1st'), (b'2nd', b'2nd'), (b'3rd', b'3rd'), (b'4th', b'4th'), (b'5th', b'5th')])),
                ('address', models.CharField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.CharField(max_length=55, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=55)),
                ('notes', models.TextField()),
            ],
            options={
                'ordering': ['precinct'],
                'verbose_name_plural': 'Precincts',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('job', models.TextField()),
                ('address', models.CharField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.CharField(max_length=55, null=True, blank=True)),
                ('notes', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=55)),
                ('contact', models.ForeignKey(related_name='unit_contact', blank=True, to='copwatch.Officer', null=True)),
                ('division', models.ForeignKey(blank=True, to='copwatch.Division', null=True)),
                ('head', models.ForeignKey(related_name='unit_commander', blank=True, to='copwatch.Officer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('car_num', models.IntegerField(unique=True, null=True, blank=True)),
                ('car_make', models.CharField(max_length=25, null=True, blank=True)),
                ('car_model', models.CharField(max_length=25, null=True, blank=True)),
                ('car_year', models.CharField(max_length=25, null=True, blank=True)),
                ('car_image', versatileimagefield.fields.VersatileImageField(storage=django.core.files.storage.FileSystemStorage(location=b'media/cops/cars'), null=True, upload_to=b'', blank=True)),
                ('image_new', models.BooleanField(default=False)),
                ('notes', models.TextField()),
                ('officers', smart_selects.db_fields.ChainedManyToManyField(chained_model_field=b'precinct', to='copwatch.Officer', chained_field=b'precinct')),
                ('precinct', models.ForeignKey(to='copwatch.Precinct')),
            ],
        ),
        migrations.AddField(
            model_name='officer',
            name='precinct',
            field=models.ForeignKey(blank=True, to='copwatch.Precinct', null=True),
        ),
        migrations.AddField(
            model_name='division',
            name='contact',
            field=models.ForeignKey(related_name='division_contact', blank=True, to='copwatch.Officer', null=True),
        ),
        migrations.AddField(
            model_name='division',
            name='head',
            field=models.ForeignKey(related_name='division_commander', blank=True, to='copwatch.Officer', null=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='officer',
            field=smart_selects.db_fields.ChainedManyToManyField(chained_model_field=b'precinct', to='copwatch.Officer', chained_field=b'precinct'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='precinct',
            field=models.ForeignKey(to='copwatch.Precinct'),
        ),
        migrations.AddField(
            model_name='bureau',
            name='contact',
            field=models.ForeignKey(related_name='bureau_contact', blank=True, to='copwatch.Officer', null=True),
        ),
        migrations.AddField(
            model_name='bureau',
            name='head',
            field=models.ForeignKey(related_name='bureau_commander', blank=True, to='copwatch.Officer', null=True),
        ),
    ]
