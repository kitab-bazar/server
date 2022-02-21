
from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from apps.book.models import Book, Author


class BookAdminForm(forms.ModelForm):
    """
    Book admin form
    """
    description_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Description [en]"))
    description_ne = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Description [ne]"), required=False
    )

    class Meta:
        model = Book
        fields = '__all__'


class AuthorAdminForm(forms.ModelForm):
    """
    Author admin form
    """
    about_author_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("About Author [en]"))
    about_author_ne = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("About author [ne]"), required=False
    )

    class Meta:
        model = Author
        fields = '__all__'
