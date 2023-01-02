from django.db.models import Manager
from .exceptions import TenantError
from .utils import state

FIELD_NAME = "shop"


class TenantManager(Manager):
    def __init__(self):
        self.state = state
        super().__init__()

    def get_queryset(self):
        current_state = self.state.get_state()
        queryset = super().get_queryset()

        if not current_state.get("enabled", True):
            return queryset

        filter_kwargs = {FIELD_NAME: self.state.get_current_tenant()}

        return queryset.filter(**filter_kwargs)

    def bulk_create(self, objs):
        tenant = self.state.get_current_tenant()

        for obj in objs:
            setattr(obj, FIELD_NAME, tenant)

        return super().bulk_create(objs)
