from django.apps import AppConfig
from django.conf import settings


class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'
    verbose_name = 'Staff Info'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from hrms import operators
            operators.data_update_start()
