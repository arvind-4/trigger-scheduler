from triggers.models import Trigger
from triggers.tasks import process_trigger
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from triggers.serializers import TriggerSerializer, TriggerViewSetSerializer


class TriggerViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    serializer_class = TriggerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Trigger.objects.filter(user=self.request.user, is_test=False)
        return TriggerViewSetSerializer(qs, many=True).data

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        process_trigger.delay(serializer.data["id"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        process_trigger.delay(serializer.data["id"])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):
        original_trigger = self.get_object()

        test_trigger = Trigger.objects.create(
            user=request.user,
            name=f"Test - {original_trigger.name}",
            trigger_type=original_trigger.trigger_type,
            interval_type=original_trigger.interval_type,
            interval_value=original_trigger.interval_value,
            fixed_time=original_trigger.fixed_time,
            endpoint=original_trigger.endpoint,
            payload_schema=original_trigger.payload_schema,
            is_test=True,
            is_recurring=False,
        )

        process_trigger.delay(test_trigger.id)

        return Response(
            {
                "message": "Test trigger created and scheduled",
                "trigger_id": test_trigger.id,
            }
        )
