from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from resizeimage import resizeimage

from django.db import models
from django.core.validators import RegexValidator
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey

from versatileimagefield.fields import VersatileImageField

from django.core.files.storage import FileSystemStorage

Fs = FileSystemStorage(location='media/cops/faces')
Cs = FileSystemStorage(location='media/cops/cars')


class Precinct(models.Model):
    TYPE = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th')
    )

    precinct = models.CharField(max_length=10, choices=TYPE)
    address = models.CharField(max_length=75, blank=True, null=True)
    # city = models.ForeignKey('cities.City')
    # organization = models.ForeignKey('digilegislature.Organization')
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=55, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=55)
    notes = models.TextField()

    def __unicode__(self):
        return u'%s Precinct' % (self.precinct)

    def name(self):
        return u'%s' % (self.precinct)

    def get_absolute_url(self):
        return "/%s/" % (self.slug)


    class Meta:
        ordering = ['precinct']
	verbose_name_plural = 'Precincts'


class Bureau(models.Model):
    TYPE = (
	('Patrol', 'Patrol'),
	('Investigations', 'Investigations'),
	('Administrative', 'Administrative')
    )

    name = models.CharField(max_length=35, choices=TYPE)
    head = models.ForeignKey('Officer', blank=True, null=True, related_name='bureau_commander')
    contact = models.ForeignKey('Officer', blank=True, null=True, related_name='bureau_contact')
    task = models.TextField()
    address = models.CharField(max_length=75, blank=True, null=True)
    # city = models.ForeignKey('cities.City')
    # organization = models.ForeignKey('digilegislature.Organization')
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=55, blank=True, null=True)
    notes = models.TextField()
    slug = models.SlugField(unique=True, max_length=55)

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return "/%s/" % (self.slug)


class Division(models.Model):
    name = models.CharField(max_length=75)
    head = models.ForeignKey('Officer', blank=True, null=True, related_name='division_commander')
    contact = models.ForeignKey('Officer', blank=True, null=True, related_name='division_contact')
    # city = models.ForeignKey('cities.City')
    # organization = models.ForeignKey('digilegislature.Organization')
    bureau = models.ForeignKey(Bureau, blank=True, null=True)
    task = models.TextField()
    address = models.CharField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=55, blank=True, null=True)
    notes = models.TextField()
    slug = models.SlugField(unique=True, max_length=55)

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return "/%s/" % (self.slug)


class Unit(models.Model):
    name = models.CharField(max_length=75)
    head = models.ForeignKey('Officer', blank=True, null=True, related_name='unit_commander')
    contact = models.ForeignKey('Officer', blank=True, null=True, related_name='unit_contact')
    # city = models.ForeignKey('cities.City')
    # organization = models.ForeignKey('digilegislature.Organization')
    division = models.ForeignKey(Division, blank=True, null=True)
    job = models.TextField()
    address = models.CharField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=55, blank=True, null=True)
    notes = models.TextField()
    slug = models.SlugField(unique=True, max_length=55)

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return "/%s/" % (self.slug)



class BasePerson(models.Model):
    EYE_COLOR = (
        ('Brown', 'Brown'),
        ('Green', 'Green'),
        ('Blue', 'Blue'),
        ('Other', 'Other'),
    )

    HAIR_COLOR = (
        ('Brown', 'Brown'),
        ('Blonde', 'Blonde'),
        ('Black', 'Black'),
        ('Grey', 'Grey'),
        ('Other', 'Other'),
    )

    STATUS = (
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced'),
    )

    FEET = (
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    )

    INCH = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    )

    RACE = (
    ('White', 'White'),
    ('Latino', 'Latino'),
    ('Black', 'Black'),
    ('Asian', 'Asian'),
    ('Mixed', 'Mixed'),
    )

    name = models.CharField(max_length=35, blank=False, null=False)
    image = VersatileImageField(storage=Fs, blank=True, null=True)
    image_new = models.BooleanField(blank=True, default=False)
    slug = models.SlugField(unique=True, max_length=125)

    ht_feet = models.CharField(max_length=5, choices=FEET, blank=True, null=True)
    ht_inch = models.CharField(max_length=5, choices=INCH, blank=True, null=True)
    weight = models.SmallIntegerField( blank=True, null=True)
    hair_color = models.CharField(max_length=6, choices=HAIR_COLOR, blank=True, null=True)
    eye_col = models.CharField(max_length=5, choices=EYE_COLOR, blank=True, null=True)
    race = models.CharField(max_length=7, choices=RACE, blank=True, null=True)
    ethnicity = models.CharField(max_length=12, blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS, blank=True, null=True)
    city_of_residence = models.CharField(max_length=55, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format: '1234567890'. Ten digits, include the area code.")
    phone = models.CharField(validators=[phone_regex], max_length="10", blank=True, null=True)
    email = models.CharField(max_length=55, blank=True, null=True)
    alma_mater = models.CharField(max_length=25, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)


    class Meta:
        abstract = True


class Officer(BasePerson):
    RANK = (
    ('Officer', 'Officer'),
    ('Sergeant', 'Sergeant'),
    ('Investigative Team Leader', 'Investigative Team Leader'),
	('Lieutenant', 'Lieutenant'),
	('Captain', 'Captain'),
	('Inspector', 'Inspector'),
	('Deputy Chief', 'Deputy Chief'),
	('Chief of Police', 'Chief of Police'),
	('Union Rep', 'Union Rep'),
	('Admin', 'Admin')
    )

    rank = models.CharField(max_length=25, choices=RANK, blank=True, null=True)
    badge_regex = RegexValidator(regex=r'^\+?1?\d{1,7}$', message="Badge number must be entered in the format: '1234567'.")
    badge = models.CharField(validators=[badge_regex], max_length=7, blank=True, null=True)
    years_emp_mps = models.SmallIntegerField( blank=True, null=True)
    years_emp_law = models.SmallIntegerField(blank=True, null=True)
    precinct = models.ForeignKey(Precinct, blank=True, null=True)
    notes = models.TextField()



    def get_absolute_url(self):
        return "/%s/%s/%s" % (self.pk, self.rank.lower(), self.slug)

    def full_name(self):
        return u'%s %s' % (self.rank, self.name)

    def get_height(self):
        return u'%sft %sin' % (self.ht_feet, self.ht_inch)

    def get_image(self):
        i = str(self.image)
        i2= i[2:]
        return i2

    def get_phone_num(self):
        i = str(self.phone)
        l = i[7:]
        m = i[3:6]
        f = i[:3]
        return u'%s-%s-%s' % (f, m, l)

    def get_car(self):
        i = Officer.objects.get(pk=self.id).vehicle_set.all()
        return i

    def __unicode__(self):
        return u'%s %s' % (self.badge, self.name)

    def save(self, *args, **kwargs):
        if self.image_new == True:
            pil_image_obj = Image.open(self.image)
            new_image = resizeimage.resize_width(pil_image_obj, 1500)

            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')

            temp_name = self.car_image.name
            self.car_image.delete(save=False)

            self.car_image.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )
        else:
            pass

        super(Officer, self).save(*args, **kwargs)

    class Meta:
        ordering = ['precinct', 'rank', 'name']
        verbose_name_plural = 'Officers'


class Vehicle(models.Model):
    car_num = models.IntegerField(blank=True, null=True, unique=True)
    car_make = models.CharField(max_length=25, blank=True, null=True)
    car_model = models.CharField(max_length=25, blank=True, null=True)
    car_year = models.CharField(max_length=25, blank=True, null=True)
    car_image = VersatileImageField(storage=Cs, blank=True, null=True)
    image_new = models.BooleanField(blank=True, default=False)
    notes = models.TextField()

    precinct = models.ForeignKey(Precinct)
    officers = ChainedManyToManyField(
            Officer,
            chained_field="precinct",
            chained_model_field="precinct",
            )

    def get_car_image(self):
        i = str(self.car_image)
        i2= i[2:]
        return i2

    def __unicode__(self):
        return u'%s %s' % (self.car_num, self.car_model)


    def save(self, *args, **kwargs):
        if self.image_new == True:
            pil_image_obj = Image.open(self.car_image)
            new_image = resizeimage.resize_width(pil_image_obj, 800)

            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')

            temp_name = self.car_image.name
            self.car_image.delete(save=False)

            self.car_image.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )
        else:
            pass

        super(Vehicle, self).save(*args, **kwargs)


class Complaint(models.Model):
    subject = models.CharField(max_length=75, blank=False, null=False)
    slug = models.SlugField(unique=True, max_length=128)
    date = models.DateTimeField(auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    location = models.CharField(max_length=75, blank=True, null=True)
    description = models.TextField()
    precinct = models.ForeignKey(Precinct)
    officer = ChainedManyToManyField(
            Officer,
            chained_field="precinct",
            chained_model_field="precinct",
            )


    def get_absolute_url(self):
        return "/%s/" % (self.slug)

    def __unicode__(self):
        return u'%s' % (self.subject)

    def name(self):
        return u'%s' % (self.subject)


    class Meta:
        ordering = ['-date', 'officer__name']
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'
