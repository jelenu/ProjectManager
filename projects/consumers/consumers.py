import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import CustomUser
from django.conf import settings
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = None

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        
        if self.user is None:
            token = data.get('token')
            if not token:
                await self.close(code=4003)
                return
            
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')

                if not user_id:
                    await self.close(code=4000)
                    return

                self.user = await self.get_user(user_id)
                if self.user is None:
                    await self.close(code=4004)
                    return

                await self.send(text_data=json.dumps({
                    'message': 'Autenticación exitosa',
                }))

            except jwt.ExpiredSignatureError:
                await self.close(code=4001)
            except jwt.InvalidTokenError:
                await self.close(code=4002)
        else:
            await self.send(text_data=json.dumps({
                'response': 'Mensaje procesado en el servidor',
                'received_data': data,
            }))

    async def disconnect(self, close_code):
        print("WebSocket desconectado con el código:", close_code)

    async def get_user(self, user_id):
        try:
            user = await database_sync_to_async(CustomUser.objects.get)(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
