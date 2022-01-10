from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import NameUniqueAbstractModel


class Tag(NameUniqueAbstractModel):

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Author name')
    )

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

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
        related_name='%(app_label)s_%(class)s_category',
        null=True,
        blank=True,
        verbose_name=_('Parent category')
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Book(models.Model):

    class LanguageType(models.TextChoices):
        NEPALI = 'nepali', 'Nepali'
        ENGLISH = 'english', 'English'

    # Basic Fields
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    categories = models.ManyToManyField(
        'book.Category', verbose_name=_('Category'), related_name='%(app_label)s_%(class)s_categories',
    )
    authors = models.ManyToManyField(
        'book.Author', verbose_name=_('Author'), related_name='%(app_label)s_%(class)s_authors',
    )
    tags = models.ManyToManyField(
        'book.Tag', verbose_name=_('Tags'), related_name='%(app_label)s_%(class)s_tags',
    )
    isbn = models.CharField(
        max_length=255,
        verbose_name=_('ISBN')
    )
    number_of_pages = models.IntegerField(verbose_name=_('Number of pages'))
    language = models.CharField(
        choices=LanguageType.choices, max_length=40, verbose_name=_('Language')
    )
    weight = models.IntegerField(verbose_name=_('Weight in grams'))
    published_date = models.DateTimeField(verbose_name=_('Published Date'))
    edition = models.CharField(
        max_length=255,
        verbose_name=_('Edition')
    )
    publisher = models.ForeignKey(
        'publisher.Publisher', verbose_name=_('Publisher'), related_name='%(app_label)s_%(class)s_publisher',
        on_delete=models.PROTECT
    )
    # TODO: need to add display price ?
    price = models.IntegerField(verbose_name=_('Price'))
    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Meta title'))
    meta_keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Meta Keywords'))
    meta_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Meta Description'))
    og_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph title'))
    og_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph description'))
    og_image = models.FileField(
        upload_to='books/', max_length=255, null=True, blank=True, default=None,
    )
    og_locale = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph locale'))
    og_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph type'))

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.title
