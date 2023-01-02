import threading
from contextlib import contextmanager
from .exceptions import TenantError


class State:
    def __init__(self):
        self.state_local = threading.local()

    def get_state(self):
        state_default = {
            "enabled": True,
            "tenant": None,
        }
        state = getattr(self.state_local, "state", state_default)
        return state

    def get_current_tenant(self):
        state = self.get_state()

        if state["enabled"] and state["tenant"] is None:
            raise TenantError("Tenant is required in context.")

        return state["tenant"]

    @contextmanager
    def tenant_context(self, tenant=None, enabled=True):
        previous_state = self.get_state()

        new_state = previous_state.copy()
        new_state["enabled"] = enabled
        new_state["tenant"] = tenant

        self.state_local.state = new_state

        try:
            yield
        finally:
            self.state_local.state = previous_state

    @contextmanager
    def tenant_context_disabled(self):
        with self.tenant_context(enabled=False):
            yield


state = State()
