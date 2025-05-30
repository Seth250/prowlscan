from rest_framework import viewsets, status
from rest_framework.response import Response

from core.models import Scan, Check, Finding
from core.serializers import ScanSerializer, CheckSerializer, FindingSerializer
from core.tasks import trigger_scan

# Create your views here.

class ScanViewSet(viewsets.ModelViewSet):
    """
    Model viewset for creating, viewing, updating and deleting scan instances.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        serializer_data = serializer.data

        headers = self.get_success_headers(serializer_data)

        scan_id = serializer_data.get('id')

        trigger_scan.delay(scan_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckViewSet(viewsets.ModelViewSet):
    """
    Model viewset for creating, viewing, updating and deleting check instances.
    """
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


class FindingViewSet(viewsets.ModelViewSet):
    """
    Model viewset for creating, viewing, updating and deleting finding instances.
    """
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer
