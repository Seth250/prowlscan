import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from core.serializers import ScanStatusSerializer

logger = logging.getLogger(__name__)

class ScanStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        self.scan_id = self.scope['url_route']['kwargs'].get('id')

        self.group_name = self.get_group_name()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    def get_group_name(self):
        return f'scan_status_{self.scan_id}'

    async def scan_message(self, event):
        serializer = ScanStatusSerializer(data={'status': event.get('status')})
        if not serializer.is_valid():
            logger.warning(f'Invalid scan status data received; Event = {event}')
            return

        await self.send(json.dumps(serializer.data))
        logger.info(f'Sent scan status websocket data for {self.scan_id}')
