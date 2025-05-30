from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your models here.

class TimeStampedModel(models.Model):
    """
    Abstract base class model that provides 'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Scan(TimeStampedModel):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'

    STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (IN_PROGRESS, _('In Progress')),
        (COMPLETED, _('Completed')),
        (FAILED, _('Failed')),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    ended_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == self.COMPLETED or self.status == self.FAILED:
            self.ended_at = timezone.now()

        super().save(*args, **kwargs)

        transaction.on_commit(self.send_websocket_events)

    def send_websocket_events(self):
        channel_layer = get_channel_layer()
        group_name = f'scan_status'

        event = {
            'type': 'scan.message',
            'id': self.id,
        }

        async_to_sync(channel_layer.group_send)(group_name, event)


class Check(TimeStampedModel):
    scan = models.ForeignKey(Scan, related_name='checks', on_delete=models.CASCADE)
    description = models.TextField(blank=True)


class Finding(TimeStampedModel):
    CRITIICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    informational = 'informational'

    SEVERITY_CHOICES = [
        (CRITIICAL, _('Critical')),
        (HIGH, _('High')),
        (MEDIUM, _('Medium')),
        (LOW, _('Low')),
        (informational, _('Informational')),
    ]

    scan_check = models.ForeignKey(Check, related_name='findings', on_delete=models.CASCADE)  # django models have a field called 'check', so we use 'scan_check' to avoid conflict
    resource_id = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default=informational)
