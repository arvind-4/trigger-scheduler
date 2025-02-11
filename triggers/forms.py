from django import forms
from triggers.models import Trigger


class TriggerForm(forms.ModelForm):
    class Meta:
        model = Trigger
        fields = [
            "name",
            "trigger_type",
            "interval_type",
            "interval_value",
            "fixed_time",
            "endpoint",
            "payload_schema",
            "is_recurring",
        ]
