from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from easy_thumbnails.files import get_thumbnailer


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images_created',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='images_liked',
        blank=True
    )

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

    def clean(self):
        super().clean()
        if not self.url and not self.image:
            raise ValidationError('You must provide either a URL or upload an image.')
        if self.url and self.image:
            raise ValidationError('Provide either a URL or upload an image, not both.')

    def get_thumbnail(self):
        if self.image:
            thumbnailer = get_thumbnailer(self.image)
            return thumbnailer.get_thumbnail({'size': (300, 0)}).url
        return None

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    indexes = [
        models.Index(fields=['-created']),
        models.Index(fields=['user']),
    ]

    def __str__(self):
        return f"Image(title={self.title}, user={self.user}, created={self.created})"
