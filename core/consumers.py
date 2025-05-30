import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import Scan
from core.serializers import ScanStatusSerializer


@database_sync_to_async
def get_scan_status(id_: int, serializer_class):
    try:
        scan = Scan.objects.get(id=id_)
    except Scan.DoesNotExist:
        scan = None

    context = {'request': None}
    serializer = serializer_class(instance=scan, context=context)
    return serializer.data


class ScanStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        self.group_name = self.get_group_name()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    def get_group_name(self):
        return f'scan_status'

    async def scan_message(self, event):
        data = await get_scan_status(id_=event['id'],
                                      serializer_class=ScanStatusSerializer)
        await self.send(json.dumps(data))
