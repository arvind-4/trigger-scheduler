from triggers.models import Trigger
from rest_framework import serializers


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        exclude = ("user", "is_test", "next_run_at")

    def validate(self, data):
        trigger_type = data.get("trigger_type")

        if trigger_type == "scheduled":
            interval_type = data.get("interval_type")
            interval_value = data.get("interval_value")
            fixed_time = data.get("fixed_time")

            if interval_type in ["minutes", "hours"] and not interval_value:
                raise serializers.ValidationError(
                    "Interval value is required for minutes/hours"
                )
            if interval_type == "fixed_time" and not fixed_time:
                raise serializers.ValidationError(
                    "Fixed time is required for fixed_time interval type"
                )

        elif trigger_type == "api":
            if not data.get("endpoint"):
                raise serializers.ValidationError(
                    "Endpoint is required for API triggers"
                )
            if not data.get("payload_schema"):
                raise serializers.ValidationError(
                    "Payload schema is required for API triggers"
                )

        return data


class TriggerViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        exclude = ("user",)
