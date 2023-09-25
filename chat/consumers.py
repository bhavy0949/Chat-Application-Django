# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .consumer_helpers import save_user_channel_name, set_user_offline, get_user_channel_name, save_chat



""" This is a completely deecoupled backend for the real-time messaging. The backend only handles the routing and message logging 
    through django channels. For testing the real-time messaging, the frontend need to have a websocket connection with the 
    backend. This can be done seperately with postman websocket request type.
    The request url will be:
        ws://localhost:8000/ws/chat/send/<user_id>/ """



class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    '''This is the method that needs to be called via frontend for websocket connection. If the user is online, the 
        connection is upgraded to websocket using this method. Once a connection is created, a private channel name 
        is stored in the user's details for the channel connection.
    '''
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        await self.accept()
        await save_user_channel_name(user_id=self.user_id, channel_name=self.channel_name)


    """ As the title says, once the disconnect() method is called from the frontend the user's private channel is
    deleted and the user is set offline. """
    
    async def disconnect(self, close_code):
        await set_user_offline(user_id = self.user_id)

    
    '''
        This is the method which handles the chat data sent over the websocket. As far as the frontend is concerned
        it's only sending data over the websocket. This method listens in over the websocket and sends the message
        to respected chatroom. 
    '''
    
    
    async def receive(self, text_data=None):
        """
        sample body:

        user 1 = {
        "message": "I'm user 1",
        "sender": "shadowmonarch",
        "send_to": 5
        }

        user 2 = {
        "message": "I'm user 2",
        "sender": "newuser",
        "send_to": 6
        }
        
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        receiver_id = text_data_json["send_to"]
        send_to = await get_user_channel_name(receiver_id)

        if send_to: #Send the message to the channel layer with both the users
            await self.channel_layer.send(
                send_to,
                {
                    'type' : 'chatroom.message',
                    'message' : message,
                    'receiver_id' : receiver_id,
                    'sender_id' : self.user_id
                }
            )
        
        else:
            print("Somthing went wrong at consumer receive method!")

    async def chatroom_message(self, event):

        # Sends message over websocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'sender_id': event['sender_id'],
                    # we can add more things here
                }
            )
        )

        # Saving message to DB
        await save_chat(event)