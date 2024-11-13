import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceptar la conexión WebSocket
        await self.accept()
        
        # Enviar un mensaje de prueba al cliente
        await self.send(text_data=json.dumps({
            'message': '¡Conexión exitosa! Este es un mensaje de prueba desde el servidor.'
        }))

    async def disconnect(self, close_code):
        # Este método se llama cuando el cliente se desconecta
        print("WebSocket desconectado con el código:", close_code)

    async def receive(self, text_data=None, bytes_data=None):
        # Maneja los mensajes recibidos del cliente
        data = json.loads(text_data)
        print("Mensaje recibido del cliente:", data)

        # Responder al cliente con un mensaje de prueba
        await self.send(text_data=json.dumps({
            'response': 'Mensaje recibido en el servidor',
            'received_data': data
        }))
