import pytz
from dateutil.parser import parse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny

from api.custom_filter import CustomLogFilter
from api.models import Log, CustomUser
from api.serializers import (
    LogSerializer,
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from caseLog import settings

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class LogView(ListModelMixin, GenericAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_class = CustomLogFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["^user__username", "^user__email"]
    filter_fields = ("log_type", "is_active")

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    @staticmethod
    def _convert_date(date_str):
        return parse(date_str).replace(tzinfo=pytz.timezone("Europe/Istanbul"))

    def get_queryset(self):
        queryset = Log.objects.all()
        created = self.request.query_params.get("created")
        user_id = self.request.query_params.get("user_id")
        company = self.request.query_params.get("company")
        if created is not None and "," in created:
            split_date = created.split(",")

            first_date, second_date = (
                f"{split_date[0]}T00:00:00.000000Z",
                f"{split_date[1]}T23:59:59.999999Z",
            )
            try:
                start, finish = self._convert_date(first_date), self._convert_date(
                    second_date
                )
            except Exception as e:
                raise ValidationError(detail=e)
            queryset = queryset.filter(created_at__gte=start, created_at__lte=finish)
        if user_id is not None:
            user_ids = user_id.split(",")
            try:
                queryset = queryset.filter(user_id__in=user_ids)
            except Exception as e:
                raise ValidationError(detail=e)
        if company is not None:
            company_ids = company.split(",")
            try:
                queryset = queryset.filter(user__company__in=company_ids)
            except Exception as e:
                raise ValidationError(detail=e)
        return queryset


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.IsAuthenticated]


class LogoutView(CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]
