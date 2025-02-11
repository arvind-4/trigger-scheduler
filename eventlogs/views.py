from rest_framework import status
from rest_framework import viewsets
from eventlogs.models import EventLog
from rest_framework.response import Response
from eventlogs.serializers import EventLogSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from eventlogs.serializers import RegisterUserSerializer


class RegisterUserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get("status", "active")
        return EventLog.objects.filter(
            trigger__user=self.request.user.id, status=status
        ).select_related("trigger")
