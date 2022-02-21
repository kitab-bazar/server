
from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from apps.blog.models import Blog


class BlogAdminForm(forms.ModelForm):
    """
    Blog admin form
    """
    description_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Description [en]"))
    description_ne = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Description [ne]"), required=False
    )

    class Meta:
        model = Blog
        fields = '__all__'
