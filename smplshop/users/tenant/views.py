from django.forms import ValidationError
from allauth.account.views import SignupView
from smplshop.users.logic import ShopForUserLogic
from .forms import TenantSignupForm
from .logic import TenantLogic


class SignupUserAndTenant(SignupView):
    template_name = "users/tenant/signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context["tenant_form"] = self.tenant_form
        return context

    def post(self, request, *args, **kwargs):
        self.tenant_form = TenantSignupForm(request.POST)
        form = self.get_form()
        if self.tenant_form.is_valid() and form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        self.tenant_form = TenantSignupForm()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ret = super().form_valid(form)
        new_tenant_logic = TenantLogic(self.tenant_form.cleaned_data["code"])
        new_tenant = new_tenant_logic.create(self.tenant_form.cleaned_data["name"])

        new_user = ShopForUserLogic(user=self.user)
        new_user.add_owned_shop(new_tenant)
        return ret
