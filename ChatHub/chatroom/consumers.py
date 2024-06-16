import json
import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

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
        message = text_data_json['message']
        # Get the username from the user's session (if authenticated)
        username = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'
        # Print the username and message to the terminal
        print(f"Message from {username}: {message}")
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username  # Include the username in the event message
            }
        )

    # Receive message from room group
    # def chat_message(self, event):
    #     message = event["message"]
    #
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({"message": message}))

        # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        date_time_obj = str(datetime.datetime.now())
        # Prepare the data you want to send
        data = {
            'message': message,
            'username': username,
            'date_time_obj': date_time_obj
            }
        # Convert the data to a JSON string
        json_data = json.dumps(data)
        # Send the JSON string to the frontend
        self.send(text_data=json_data)



