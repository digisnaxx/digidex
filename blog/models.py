from django.db import models
from twitter import *
# from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.utils.text import slugify
# from accounts.models import User
from soc_keys import TWITTER_TOKEN, TWITTER_TOKEN_KEY, CON_SECRET, CON_SECRET_KEY

from versatileimagefield.fields import VersatileImageField

from django.core.files.storage import FileSystemStorage

Ps = FileSystemStorage(location='media/posts/img')
Vs = FileSystemStorage(location='media/posts/vid')

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField()

    # def save(self):
    # if not self.slug:
    # self.slug = slugify(unicode(self.name))
    # 	super(Category, self).save()

    class Meta:
        ordering = ['slug']
        verbose_name = "DigiBin"
        verbose_name_plural = "DigiBins"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/%s/" % self.slug


class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Tags"
        verbose_name_plural = "Tags"

    def save(self):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Tag, self).save()

    def get_absolute_url(self):
        return "/tag/%s/" % (self.slug)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=False)
    focus = models.CharField(max_length=55, blank=True, null=True)
    content = models.TextField()
    slug = models.SlugField(unique=True, max_length=255)
    #creator = models.ForeignKey(User, blank=True, null=True)
    org = models.ForeignKey('digilegislature.Organization', blank=True, null=True, related_name='orgs')
    affiliates = models.ManyToManyField('digilegislature.Organization', blank=True, related_name='affils')
    twit = models.BooleanField(default=False)
    image = VersatileImageField(storage=Ps, blank=True, null=True)
    video = models.FileField(storage=Vs, null=True, blank=True)
    sound_cloud = models.CharField(max_length=25, null=True, blank=True)
    video_type = models.CharField(max_length=4, null=True, blank=True)
    # site = models.ForeignKey(Site)
    published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Snaxx"
        verbose_name_plural = "Snaxx"

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.slug)

    def get_image(self):
        i = str(self.image)
        i2= i[2:]
        return i2

    def save(self, *args, **kwargs):
        t = Twitter(auth=OAuth(TWITTER_TOKEN, TWITTER_TOKEN_KEY, CON_SECRET, CON_SECRET_KEY))
        s = self.title
        l = 'www.digisnaxx.com' + self.get_absolute_url()
        full_post = s + ' ' + l
        if self.twit is not False:
            t.statuses.update(status=full_post)
        super(Post, self).save(*args, **kwargs)
