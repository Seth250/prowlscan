from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(r'scans', viewsets.ScanViewSet, basename='scan')
router.register(r'checks', viewsets.CheckViewSet, basename='check')
router.register(r'findings', viewsets.FindingViewSet, basename='finding')

urlpatterns = router.urls
