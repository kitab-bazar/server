from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.common import get_social_sharable_image


class Tag(models.Model):

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        unique=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Category name')
    )
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='blog_category',
        null=True,
        blank=True,
        verbose_name=_('Parent category')
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Blog(models.Model):

    class BlogPublishType(models.TextChoices):
        PUBLISH = 'publish', 'Publish'
        DRAFT = 'draft', 'Draft'

    title = models.TextField(blank=True, verbose_name=_('Blog title'))
    description = models.TextField(blank=True, verbose_name=_('Blog Description'))
    image = models.FileField(
        upload_to='blog/images/', max_length=255, null=True, blank=True, default=None,
        verbose_name=_('Blog image')
    )
    category = models.ForeignKey(
        'blog.Category', on_delete=models.CASCADE,
        related_name='blog_categories', verbose_name=_('Blog category')
    )
    tags = models.ManyToManyField(
        'blog.Tag', related_name='blog_tags', blank=True, verbose_name=_('Blog Tags')
    )
    published_date = models.DateField(verbose_name=_('Published Date'))
    blog_publish_type = models.CharField(
        choices=BlogPublishType.choices, max_length=40, verbose_name=_('Publish Type'), default=BlogPublishType.DRAFT
    )
    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Meta title'))
    meta_keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Meta Keywords'))
    meta_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Meta Description'))
    og_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph title'))
    og_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph description'))
    og_image = models.FileField(
        upload_to='blog/og_image/', max_length=255, null=True, blank=True, default=None,
    )
    og_locale = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph locale'))
    og_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph type'))

    # Session to check if image changed to generate og image
    __image_name = None

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__image_name = self.image.name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image and self.image.name != self.__image_name:
            filename = f'og_{self.image.name.split("/")[-1]}'
            social_sharable_image = get_social_sharable_image(self.image, filename)
            self.og_image.save(filename, social_sharable_image, save=False)
        super(Blog, self).save(*args, **kwargs)
