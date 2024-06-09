"""The file upload form."""

from django import forms


class TagForm(forms.Form):
    """The file upload form."""

    tags = forms.CharField(label="Seperate multiple tags with comma, enclose tags with spaces in quotes.")
