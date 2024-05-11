
class AlbumView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """The upload view of many files."""

    template_name = "upload.html"
    form_class = UploadForm


