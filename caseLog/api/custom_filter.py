import django_filters
from django.db.models import Q
import pytz
from dateutil.parser import parse
from rest_framework.exceptions import ValidationError

from api.models import Log
from api.utils import convert_date


class CustomLogFilter(django_filters.FilterSet):
    log_type = django_filters.TypedChoiceFilter(
        field_name="log_type",
        choices=[("login", "login"), ("logout", "logout")],
    )
    is_active = django_filters.BooleanFilter(field_name="user__is_active")
    created = django_filters.CharFilter(method="custom_datetime_range_filter")
    user_id = django_filters.CharFilter(method="custom_user_id_filter")
    company = django_filters.CharFilter(method="custom_company_id_filter")

    @staticmethod
    def custom_datetime_range_filter(queryset, _, value):
        split_date = value.split(",")
        first_date, second_date = (
            f"{split_date[0]}T00:00:00.000000Z",
            f"{split_date[1]}T23:59:59.999999Z",
        )
        try:
            start, finish = convert_date(first_date), convert_date(second_date)
            return queryset.filter(created_at__gte=start, created_at__lte=finish)
        except Exception as e:
            raise ValidationError(detail=e)

    @staticmethod
    def custom_user_id_filter(queryset, _, value):
        user_ids = value.split(",")
        try:
            return queryset.filter(user_id__in=user_ids)
        except Exception as e:
            raise ValidationError(detail=e)

    @staticmethod
    def custom_company_id_filter(queryset, _, value):
        company_ids = value.split(",")
        try:
            return queryset.filter(user__company__in=company_ids)
        except Exception as e:
            raise ValidationError(detail=e)

    class Meta:
        model = Log
        fields = ["log_type", "is_active", "created", "user_id", "company"]
