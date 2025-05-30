from celery import shared_task

from prowler.providers.aws.aws_provider import AWSProvider
from prowler.lib.scan.scan import Scan as ProwlerScan

from core.models import Scan


@shared_task
def trigger_scan(regions: set | None = None):
    if regions is None:
        regions = {}

    provider = AWSProvider(regions=regions)
    scan = Scan.objects.create(status=Scan.IN_PROGRESS)

    prowler_scan = ProwlerScan(provider=provider).scan()
