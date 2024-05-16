"""The file upload form."""
from typing import ClassVar

from django import forms
from utils.filefield import MultipleFileField

from .models import BaseFile


class UploadForm(forms.ModelForm[BaseFile]):
    """The file upload form."""

    files = MultipleFileField(label="Select file(s) *")  # type: ignore[assignment]

    class Meta:
        """Set model and fields."""

        model = BaseFile
        fields = ("license", "attribution")
        labels: ClassVar[dict[str, str]] = {
            "license": "License *",
            "attribution": "Attribution *",
        }
        widgets: ClassVar[dict[str, forms.Select | forms.TextInput]] = {
            "license": forms.Select(attrs={"onchange": "enableUploadButton()"}),
            "attribution": forms.TextInput(attrs={"placeholder": "Attribution", "onchange": "enableUploadButton()"}),
        }


class UpdateForm(forms.ModelForm[BaseFile]):
    """The file update form."""

    class Meta:
        """Set model and fields."""

        model = BaseFile
        fields = ("title", "attribution", "description")
