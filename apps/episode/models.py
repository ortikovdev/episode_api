import os
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from apps.account.models import User


class BaseModel(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Tag(BaseModel):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Episode(BaseModel):
    title = models.CharField(max_length=221)
    slug = models.SlugField(max_length=221)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='episode', null=True, blank=True)
    music = models.FileField(upload_to='episodes/', validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return mark_safe(
                f'<a href="{self.image.url}" target="_blank"><img src="{self.image.url}" width="50" height="50" /></a>')
        return '-'

    @property
    def music_absolute_path(self):
        return os.getenv('SITE_DOMAIN') + self.music.url


class EpisodeComment(BaseModel):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    top_level_comment_id = models.IntegerField(null=True, blank=True)

    @property
    def get_children(self):
        model = self.__class__
        return model.objects.filter(top_level_comment_id=self.id)


class EpisodeLike(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


def make_slugify(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f"{slug}-{qs.count()}"
        return make_slugify(instance, new_slug=slug)
    instance.slug = slug


@receiver(pre_save, sender=EpisodeComment)
def comment_pre_save(sender, instance, *args, **kwargs):
    if instance.parent:
        if not instance.parent.top_level_comment_id:
            instance.top_level_comment_id = instance.parent_id
        else:
            instance.top_level_comment_id = instance.parent.top_level_comment_id