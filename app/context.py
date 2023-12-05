"""
Custom Bot class that allows for a custom update type.
"""
from telegram.ext import CallbackContext, ExtBot, Application


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates of type
    `WebhookUpdate`.
    """

    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        return super().from_update(update, application)
