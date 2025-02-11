# backend/triggers/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Trigger
from eventlogs.models import EventLog
from .serializers import TriggerSerializer, EventLogSerializer
from .tasks import process_trigger

class TriggerViewSet(viewsets.ModelViewSet):
    serializer_class = TriggerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trigger.objects.filter(user=self.request.user, is_test=False)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        process_trigger.delay(serializer.data['id'])
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        original_trigger = self.get_object()
        
        # Create a test copy of the trigger
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
            is_recurring=False
        )
        
        # Process the test trigger
        process_trigger.delay(test_trigger.id)
        
        return Response({
            'message': 'Test trigger created and scheduled',
            'trigger_id': test_trigger.id
        })

class EventLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        status = self.request.query_params.get('status', 'active')
        return EventLog.objects.filter(
            trigger__user=self.request.user,
            status=status
        ).select_related('trigger')