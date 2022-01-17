
from django import forms
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE
from apps.book.models import Book


class BookAdminForm(forms.ModelForm):
    """
    Book admin form
    """
    description_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Description"))
    description_ne = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Description [ne]"), required=False
    )

    class Meta:
        model = Book
        fields = '__all__'
