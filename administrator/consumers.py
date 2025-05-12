import json
from channels.generic.websocket import WebsocketConsumer
from home_page.models import FoundItem, LostItem, MatchedItem
from asgiref.sync import async_to_sync
from django.db.models import Count

class StatsConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'reports'
        self.accept()
        # Add the WebSocket to the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.send_initial_counts()

    def disconnect(self, close_code):
        # Remove the WebSocket from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # def receive(self, text_data):
    #     # Handle incoming WebSocket messages (if needed)
    #     data = json.loads(text_data)
    #     self.send(text_data=json.dumps({
    #         'message': 'Message received!',
    #         'data': data
    #     }))

    def send_report_update(self, event):
        # Send a message to the WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'total_found': event['total_found'],
            'total_lost': event['total_lost'],
            'total_matched': event['total_matched'],
        }))

    def send_report_update(self, event):
        # Get updated category data
        category_data = list(
            LostItem.objects.values('category')
            .annotate(count=Count('category'))
            .order_by('category')
        )

        # Send updated counts to the WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'total_found': event['total_found'],
            'total_lost': event['total_lost'],
            'total_matched': event['total_matched'],
            'category_data': category_data,  # Add category data if present
        }))

    def send_initial_counts(self):
        # Fetch the initial counts
        total_found = FoundItem.objects.count()
        total_lost = LostItem.objects.count()
        total_matched = MatchedItem.objects.count()

        # Fetch category data
        category_data = list(
            LostItem.objects.values('category')
            .annotate(count=Count('category'))
            .order_by('category')
        )

        # Send the initial counts to the WebSocket
        self.send(text_data=json.dumps({
            'message': 'Initial counts',
            'total_found': total_found,
            'total_lost': total_lost,
            'total_matched': total_matched,
            'category_data': category_data,
        }))