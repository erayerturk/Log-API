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
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    filter_fields = ("log_type", "is_active", "created", "user_id", "company")

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


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
