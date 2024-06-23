"""Album views."""
import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms import Form
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from files.filters import FileFilter
from files.forms import FileMultipleActionForm
from files.models import BaseFile
from files.tables import FileTable
from guardian.shortcuts import get_objects_for_user
from hitcounter.utils import count_hit
from utils.mixins import CuratorGroupRequiredMixin

from .filters import AlbumFilter
from .forms import AlbumAddFilesForm
from .models import Album
from .tables import AlbumTable

logger = logging.getLogger("bma")


class AlbumListView(SingleTableMixin, FilterView):
    """Album list view."""

    model = Album
    table_class = AlbumTable
    template_name = "album_list.html"
    filterset_class = AlbumFilter
    context_object_name = "albums"

    def get_queryset(self) -> models.QuerySet[Album]:
        """Use bmanager to get rich album objects."""
        return Album.bmanager.all()


class AlbumDetailView(SingleTableMixin, FilterView):
    """Album detail view with file table and filter."""

    pk_url_kwarg = "album_uuid"
    template_name = "album_detail.html"
    table_class = FileTable
    filterset_class = FileFilter

    def get_template_names(self) -> list[str]:
        """Template name depends on the type of detailview."""
        return [f"{self.request.resolver_match.url_name}.html"]

    def get_object(self, queryset: models.QuerySet[Album] | None = None) -> Album:
        """Use the manager so the album object has prefetched active_files."""
        album = Album.bmanager.get(pk=self.kwargs["album_uuid"])
        # count the hit
        count_hit(self.request, album)
        return album  # type: ignore[no-any-return]

    def get_queryset(self) -> str:
        """Prefer a real bmanager qs over the list of files so each file obj has all needed info."""
        uuids = [f.pk for f in self.get_object().active_files_list]  # type: ignore[attr-defined]
        return BaseFile.bmanager.get_permitted(user=self.request.user).filter(pk__in=uuids)  # type: ignore[no-any-return]

    def get_context_data(self, **kwargs: dict[str, str]) -> dict[str, str]:
        """Add album to context."""
        context = super().get_context_data(**kwargs)
        context["album"] = self.get_object()
        context["file_action_form"] = FileMultipleActionForm()
        return context  # type: ignore[no-any-return]


class AlbumCreateView(CuratorGroupRequiredMixin, CreateView):  # type: ignore[type-arg]
    """Album create view."""

    template_name = "album_form.html"
    model = Album
    fields = ("title", "description")

    def get_form(self, form_class: Any | None = None) -> Form:  # noqa: ANN401
        """Return an instance of the form to be used in this view, only show permitted files in the form."""
        form = super().get_form()
        form.fields["files"].queryset = BaseFile.bmanager.get_permitted(user=self.request.user)
        return form  # type: ignore[no-any-return]

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        """Set album owner before saving."""
        album = form.save(commit=False)  # type: ignore[attr-defined]
        album.owner = self.request.user
        album.save()
        form.save_m2m()  # type: ignore[attr-defined]
        messages.success(self.request, f"Album {album.pk} created!")
        return HttpResponseRedirect(album.get_absolute_url())


class AlbumUpdateView(CuratorGroupRequiredMixin, UpdateView):  # type: ignore[type-arg]
    """Album update view."""

    template_name = "album_form.html"
    model = Album
    fields = ("title", "description", "files")
    pk_url_kwarg = "album_uuid"

    def get_form(self, form_class: Any | None = None) -> Form:  # noqa: ANN401
        """Return an instance of the form to be used in this view, only show permitted files in the form."""
        form = super().get_form()
        form.fields["files"].queryset = BaseFile.bmanager.get_permitted(user=self.request.user)
        return form  # type: ignore[no-any-return]

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        """Set album owner before saving."""
        album = form.save(commit=False)  # type: ignore[attr-defined]
        album.owner = self.request.user
        album.save()
        album.update_members(*[f.pk for f in form.cleaned_data["files"]], replace=False)
        return HttpResponseRedirect(album.get_absolute_url())


class AlbumAddFilesView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """Add files to an album."""

    form_class = AlbumAddFilesForm

    def get_form(self, form_class: AlbumAddFilesForm | None = None) -> AlbumAddFilesForm:  # type: ignore[override]
        """Return an instance of the form vith appropriate choices."""
        form = super().get_form()
        form.fields["files_to_add"].choices = BaseFile.bmanager.get_permitted(user=self.request.user).values_list(
            "pk", "pk"
        )
        form.fields["album"].choices = get_objects_for_user(self.request.user, "change_album", klass=Album).values_list(
            "pk", "title"
        )
        return form  # type: ignore[no-any-return]

    def form_valid(self, form: Form) -> HttpResponse:
        """Add the files and redirect to the album detail page."""
        album = Album.objects.get(pk=form.cleaned_data["album"])
        if not self.request.user.has_perm("change_album", album):
            raise PermissionDenied
        album.files.add(*form.cleaned_data["files_to_add"])
        messages.success(self.request, f"Added {len(form.cleaned_data['files_to_add'])} file(s) to album {album.title}")
        return redirect(album)

    def form_invalid(self, form: Form) -> HttpResponse:
        """Return an error message and redirect back to file list."""
        messages.error(self.request, "Something is fucky with the form")
        return redirect(reverse("files:file_list"))
