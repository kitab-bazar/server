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


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Author name')
    )
    about_author = models.TextField(null=True, blank=True, verbose_name=_('About author'))

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
        related_name='book_category',
        null=True,
        blank=True,
        verbose_name=_('Parent category')
    )
    image = models.FileField(
        upload_to='books/category/images/', max_length=255, null=True, blank=True, default=None,
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Book(models.Model):

    class LanguageType(models.TextChoices):
        ENGLISH = 'english', _('English')
        NEPALI = 'nepali', _('Nepali')
        MAITHALI = 'Maithali', _('Maithali')
        THARU = 'Tharu', _('Tharu')
        BILINGUAL = 'bilingual', _('Bilingual')

    class Grade(models.TextChoices):
        ECD = 'ecd', _('ECD')
        GRADE_1 = 'grade_1', _('Grade 1')
        GRADE_2 = 'grade_2', _('Grade 2')
        GRADE_3 = 'grade_3', _('Grade 3')
        GRADE_4 = 'grade_4', _('Grade 4')
        GRADE_5 = 'grade_5', _('Grade 5')

    # Basic Fields
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    image = models.FileField(
        upload_to='books/images/', max_length=255, null=True, blank=True, default=None,
    )
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    categories = models.ManyToManyField(
        'book.Category', verbose_name=_('Category'), related_name='%(app_label)s_%(class)s_categories',
    )
    authors = models.ManyToManyField(
        'book.Author', verbose_name=_('Author'), related_name='%(app_label)s_%(class)s_authors',
    )
    tags = models.ManyToManyField(
        'book.Tag', verbose_name=_('Tags'), related_name='%(app_label)s_%(class)s_tags', blank=True
    )
    isbn = models.CharField(
        max_length=13,
        verbose_name=_('ISBN'),
        blank=True,
    )
    number_of_pages = models.IntegerField(verbose_name=_('Number of pages'))
    language = models.CharField(
        choices=LanguageType.choices, max_length=40, verbose_name=_('Language')
    )
    weight = models.IntegerField(verbose_name=_('Weight in grams'), null=True, blank=True)
    published_date = models.DateField(verbose_name=_('Published Date'))
    edition = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Edition')
    )
    publisher = models.ForeignKey(
        'publisher.Publisher', verbose_name=_('Publisher'), related_name='%(app_label)s_%(class)s_publisher',
        on_delete=models.PROTECT
    )
    grade = models.CharField(
        choices=Grade.choices, max_length=40, verbose_name=_('Grade'), null=True, blank=True
    )
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
    created_by = models.ForeignKey(
        'user.User', verbose_name=_('Created by'), related_name='book_creator', null=True, blank=True,
        on_delete=models.CASCADE
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
        upload_to='books/og_image/', max_length=255, null=True, blank=True, default=None,
    )
    og_locale = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph locale'))
    og_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Open graph type'))

    # Session to check if image changed to generate og image
    __image_name = None

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

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
        super(Book, self).save(*args, **kwargs)


class WishList(models.Model):
    created_by = models.ForeignKey(
        'user.User', verbose_name=_('User'), related_name='wish_lists',
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        'book.Book', verbose_name=_('Book'), related_name='book_wish_list',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Wish list')
        verbose_name_plural = _('Wish lists')

    def __str__(self):
        return f'{self.created_by} - {self.book}'
