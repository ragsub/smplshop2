from django.apps import AppConfig


class TenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smplshop.users.tenant'
