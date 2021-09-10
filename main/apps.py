from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    # Customise app name in Django admin panel
    verbose_name = 'blog management'
