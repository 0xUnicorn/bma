"""File views."""
import logging
import re
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.forms import Form
from django.http import FileResponse
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from tags.filters import TagFilter
from tags.forms import TagForm
from tags.mixins import TagViewMixin
from tags.models import TaggedFile
from tags.tables import TaggingTable
from tags.tables import TagTable

from .filters import FileFilter
from .forms import UpdateForm
from .forms import UploadForm
from .mixins import FileViewMixin
from .models import BaseFile
from .tables import FileTable

logger = logging.getLogger("bma")


class FileUploadView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """The upload view of many files. Uses the API and a js client to upload."""

    template_name = "upload.html"
    form_class = UploadForm


class FileListView(SingleTableMixin, FilterView):
    """File list view."""

    table_class = FileTable
    template_name = "file_list.html"
    filterset_class = FileFilter
    context_object_name = "files"

    def get_queryset(self) -> QuerySet[BaseFile]:
        """Get files that are approved, published and not deleted, or where the current user has view_basefile perms."""
        return BaseFile.bmanager.get_permitted(user=self.request.user).all()  # type: ignore[no-any-return]


class FileDetailView(DetailView):  # type: ignore[type-arg]
    """File detail view. Shows a single file."""

    template_name = "detail.html"
    model = BaseFile
    pk_url_kwarg = "file_uuid"
    context_object_name = "file"

    def get_object(self, queryset: QuerySet[BaseFile] | None = None) -> BaseFile:
        """Check permissions before returning the file."""
        basefile = super().get_object(queryset=queryset)
        if not basefile.permitted(user=self.request.user):
            # the current user does not have permissions to view this file
            raise PermissionDenied
        return basefile  # type: ignore[no-any-return]


class FileDeleteView(LoginRequiredMixin, DeleteView):  # type: ignore[type-arg,misc]
    """File softdelete view. Softdelete a single file."""

    template_name = "delete.html"
    model = BaseFile
    pk_url_kwarg = "file_uuid"

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        """Check permissions before soft deleting file."""
        if not self.request.user.has_perm("files.delete_basefile", self.object):
            raise PermissionDenied
        self.object.softdelete()
        return HttpResponseRedirect(reverse_lazy("files:file_detail", kwargs={"file_uuid": self.object.uuid}))


class FileUpdateView(LoginRequiredMixin, UpdateView):  # type: ignore[type-arg]
    """File update view. Update a single files attributes."""

    template_name = "update.html"
    model = BaseFile
    form_class = UpdateForm
    pk_url_kwarg = "file_uuid"

    def get_object(self, queryset: QuerySet[BaseFile] | None = None) -> BaseFile:
        """Check permissions before returning the file."""
        basefile = super().get_object(queryset=queryset)
        if not self.request.user.has_perm("files.change_basefile", basefile):
            raise PermissionDenied
        return basefile  # type: ignore[no-any-return]


def bma_media_view(request: HttpRequest, path: str, *, accel: bool) -> FileResponse | HttpResponse:
    """Serve media files using nginx x-accel-redirect, or serve directly for dev use."""
    # get last uuid from the path
    match = re.match(
        r"^.*([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}).*$",
        path,
    )
    if not match:
        # regex parsing failed
        logger.debug("Unable to parse filename regex to find file UUID, returning 404")
        raise Http404

    # get the file from database
    try:
        dbfile = BaseFile.objects.get(uuid=match.group(1))
    except BaseFile.DoesNotExist as e:
        logger.debug(
            f"File UUID {match.group(1)} not found in database, returning 404",
        )
        raise Http404 from e

    # check file permissions
    if not dbfile.permitted(user=request.user):
        # the current user does not have permissions to view this file
        raise PermissionDenied

    # check if the file exists in the filesystem
    if not Path(dbfile.original.path).exists():
        raise Http404

    # OK, show the file
    response: FileResponse | HttpResponse
    if accel:
        # we are using nginx x-accel-redirect
        response = HttpResponse(status=200)
        # remove the Content-Type header to allow nginx to add it
        del response["Content-Type"]
        response["X-Accel-Redirect"] = f"/public/{quote(path)}"
    else:
        # we are serving the file locally
        f = Path.open(Path(settings.MEDIA_ROOT) / Path(path), "rb")
        response = FileResponse(f, status=200)
    # all good
    return response


class FileBrowserView(TemplateView):
    """The file browser view."""

    template_name = "filebrowser.html"


########## File tag views ######################################################


class FileTagListView(SingleTableMixin, FilterView):
    """File tag list view."""

    table_class = TagTable
    template_name = "file_tags.html"
    filterset_class = TagFilter
    context_object_name = "tags"

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Get file object from url."""
        self.file = get_object_or_404(BaseFile.bmanager.get_permitted(user=request.user), uuid=kwargs["file_uuid"])
        super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[BaseFile]:
        """Get tags for this file."""
        return self.file.tags.weighted.all()  # type: ignore[no-any-return]


class CuratorGroupRequiredMixin:
    """This mixin makes views only accessible by users in the curators group."""

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Check for membership of settings.BMA_CURATOR_GROUP_NAME and raise PermissionDenied if needed."""
        curator_group, created = Group.objects.get_or_create(name=settings.BMA_CURATOR_GROUP_NAME)
        if curator_group not in request.user.groups.all():  # type: ignore[union-attr]
            raise PermissionDenied
        super().setup(request, *args, **kwargs)  # type: ignore[misc]


class FileTagCreateView(CuratorGroupRequiredMixin, FileViewMixin, FormView):  # type: ignore[type-arg]
    """View to add one or more tags to a file."""

    form_class = TagForm
    template_name = "file_tag_create.html"

    def form_valid(self, form: TagForm) -> HttpResponse:
        """Apply the tag(s)."""
        self.file.parse_and_add_tags(tags=form.cleaned_data["tags"], tagger=self.request.user)
        messages.success(self.request, "Tag(s) added.")
        return redirect(self.file)


class FileTagDetailView(FileViewMixin, TagViewMixin, SingleTableMixin, ListView):  # type: ignore[type-arg]
    """File tag detail view. Shows a list of taggings of a single tag on a file."""

    table_class = TaggingTable
    template_name = "file_tagging_list.html"
    model = TaggedFile


class FileTagDeleteView(TagViewMixin, FileViewMixin, DeleteView):  # type: ignore[type-arg,misc]
    """File untagging view. Removes a users tagging of a tag from a file."""

    model = TaggedFile

    def get_object(self, queryset: QuerySet[TaggedFile] | None = None) -> TaggedFile:
        """Get the TaggedFile object if it exists."""
        return get_object_or_404(self.file.taggings.all(), tag=self.tag, tagger=self.request.user)  # type: ignore[no-any-return]

    def form_valid(self, form: Form) -> HttpResponse:
        """Untag and redirect to file details."""
        self.object.delete()
        messages.success(self.request, "Tag deleted.")
        return redirect(self.file)
