from rest_framework import viewsets

from core.models import Scan, Check, Finding
from core.serializers import ScanSerializer, CheckSerializer, FindingSerializer

# Create your views here.

class ScanViewSet(viewsets.ModelViewSet):
    """
    Model viewset for creating, viewing, updating and deleting scan instances.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer


class CheckViewSet(viewsets.ModelViewSet):
    """
    Model viewset for creating, viewing, updating and deleting check instances.
    """
    serializer_class = CheckSerializer

    def get_queryset(self):
        scan_id = self.kwargs.get('scan_pk')
        if scan_id:
            return self.queryset.filter(scan_id=scan_id)
        return self.queryset


class FindingViewSet(viewsets.ModelViewSet):
    """
    Model viewset for creating, viewing, updating and deleting finding instances.
    """
    serializer_class = FindingSerializer

    def get_queryset(self):
        check_id = self.kwargs.get('check_pk')
        if check_id:
            return self.queryset.filter(check_id=check_id)
        return self.queryset