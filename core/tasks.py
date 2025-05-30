from celery import shared_task

from prowler.providers.aws.aws_provider import AwsProvider
from prowler.lib.scan.scan import Scan as ProwlerScan

from core.models import Scan


@shared_task
def trigger_scan(scan_id: int, regions: set | None = None):
    if regions is None:
        regions = {}

    provider = AwsProvider(regions=regions)
    scan = Scan.objects.get(id=scan_id)
    scan.status = Scan.IN_PROGRESS
    scan.save()

    # ran into credential issues
    # prowler_scan = ProwlerScan(provider=provider).scan()

    scan.status = Scan.COMPLETED
    scan.save()
