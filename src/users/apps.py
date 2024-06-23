"""AppConfig for the users app."""

from django.apps import AppConfig
from django.core.signals import request_started


class UsersConfig(AppConfig):
    """AppConfig for the users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        """Connect signal to create groups on first request."""
        from utils.signals import bma_startup

        request_started.connect(bma_startup, dispatch_uid="bma_startup_signal")
