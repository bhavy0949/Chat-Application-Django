from api.models import Users
from channels.db import database_sync_to_async
from .models import MessageRecord

@database_sync_to_async
def save_user_channel_name(user_id, channel_name):
    try:
        user = Users.objects.get(pk=user_id)
        user.private_channel_name = channel_name
        user.save()
        return True
    except Exception as E:
        print(E)
        return
    

@database_sync_to_async
def get_user_channel_name(user_id):
    try:
        return Users.objects.get(pk=user_id).private_channel_name
    except Exception as E:
        print(E)
        return
    

    

@database_sync_to_async
def set_user_offline(user_id):
    try:
        user =Users.objects.get(pk=user_id)
        user.is_online = False
        user.private_channel_name = None
        user.save()

    except Exception as E:
        print(E)
        return

@database_sync_to_async
def save_chat(message_obj):
    sender_id, receiver_id = message_obj['sender_id'], message_obj['receiver_id']
    users = Users.objects.filter(pk__in=[sender_id,receiver_id])

    if users[0] == message_obj['sender_id']:
        sender = users[0]
        receiver = users[1]

    else:
        sender = users[1]
        receiver = users[0]

    #Create a message record
    message_record = MessageRecord(
        sender = sender,
        receiver = receiver,
        message = message_obj['message'],
        #These fields can be worked on the frontend
        message_type = "text",
        is_read = False,
        is_delivered = False,
        is_deleted = False

    )
    message_record.save()