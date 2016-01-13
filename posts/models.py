import os
import random
import string

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils import timezone


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(published_at__lte=timezone.now(), draft=False)


def upload_location(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return '{model_name}s/{owner_id}/{random_filename}{file_extension}'.format(model_name=str(instance.__class__.__name__).lower(), owner_id=instance.user.id, random_filename=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)), file_extension=file_extension)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()

    def get_absolute_url(self):
        return reverse('posts:show', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at', '-updated_at']


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)

    if new_slug is not None:
        slug = new_slug
    
    querySet = Post.objects.filter(slug=slug).order_by('-id')
    exists = querySet.exists()
    if exists:
        new_slug = "{}-{}".format(slug, querySet.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)