from eventlogs.models import EventLog
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password2"]
        )
        return user


class EventLogSerializer(serializers.ModelSerializer):
    trigger_name = serializers.CharField(source="trigger.name", read_only=True)

    class Meta:
        model = EventLog
        fields = "__all__"
        read_only_fields = ("trigger", "status", "is_test")
