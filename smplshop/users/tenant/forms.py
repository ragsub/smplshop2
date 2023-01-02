from django.forms import ModelForm, CharField, TextInput
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator

from .models import Shop


class TenantSignupForm(ModelForm):
    class Meta:
        model = Shop
        fields = ["code", "name"]
