from django.http.request import HttpRequest
from django.http import Http404
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from smplshop.users.logic import ShopForUserLogic

from .logic import TenantContextLogic
from .utils import state


class GetShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        tenant_context = TenantContextLogic(request.user, request.path)  # type:ignore

        # check if tenant context is required:
        if tenant_context.is_required():
            shop = tenant_context.get_shop()
            if shop is not None:
                request.shop = shop  # type:ignore
                with state.tenant_context(shop):
                    response = self.get_response(request)

            else:
                logout(request)
                raise Http404(_("Shop does not exist"))

        else:
            with state.tenant_context_disabled():
                response = self.get_response(request)

        return response
