import django_filters

from api.models import Log


class CustomLogFilter(django_filters.FilterSet):
    log_type = django_filters.TypedChoiceFilter(
        field_name="log_type",
        choices=[("login", "login"), ("logout", "logout")],
    )
    is_active = django_filters.BooleanFilter(field_name="user__is_active")

    class Meta:
        model = Log
        fields = ["log_type", "is_active"]
