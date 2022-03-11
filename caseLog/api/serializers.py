from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import CustomUser, Company, Log


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "is_active"]


class LogSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    company = serializers.CharField(
        source="user.company.name", allow_null=False, allow_blank=False
    )
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Log
        fields = [
            "company",
            "user",
            "created_at",
            "log_type",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    company = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "password", "password2", "email", "company")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        company = Company.objects.get_or_create(name=validated_data["company"])
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            company=company[0],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = []

    def create(self, _):
        user = CustomUser.objects.get(username=self.context["request"].user)
        log = Log.objects.create(log_type="login", user=user)
        return log


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = []

    def create(self, _):
        user = CustomUser.objects.get(username=self.context["request"].user)
        log = Log.objects.create(log_type="logout", user=user)
        return log
