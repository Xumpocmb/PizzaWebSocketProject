import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Order


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "orders"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        order_id = text_data_json['order_id']
        print('Received data:', order_id)
        # Отправка данных в группу
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'orders_update', 'order_id': order_id}
        )
        print('Sent data to group:', self.room_group_name)

    # Обработка данных от группы
    def orders_update(self, event):
        # Отправка данных обновления клиенту
        order_id = event['order_id']
        print('Received order_id from group:', order_id)

        order = Order.objects.filter(pk=order_id).first()

        # Отправка данных обновления клиенту
        self.send(text_data=json.dumps({
            'order_id': order.id,
            'customer_name': order.customer_name,
        }))
        print('Sent data to client:', order_id)


