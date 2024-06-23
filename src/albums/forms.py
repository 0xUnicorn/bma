"""The forms used in the albums app."""

from django import forms


class AlbumAddFilesForm(forms.Form):
    """This form is used to add files to an existing album."""

    album = forms.ChoiceField(
        widget=forms.RadioSelect,
    )

    files_to_add = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"class": "d-none"}),
    )
