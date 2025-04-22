import asyncio
import websockets
import json
import mysql.connector
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.clients = {}  # {user_id: websocket}
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='naitik@mysql',
            database='saathi'
        )
        self.cursor = self.db.cursor(dictionary=True)

    async def register(self, websocket, user_id):
        self.clients[user_id] = websocket
        print(f"User {user_id} connected")

    async def unregister(self, user_id):
        if user_id in self.clients:
            del self.clients[user_id]
            print(f"User {user_id} disconnected")

    async def send_message(self, sender_id, receiver_id, message):
        try:
            # Store message in database
            self.cursor.execute("""
                INSERT INTO Messages (sender_id, receiver_id, message, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (sender_id, receiver_id, message, datetime.now()))
            self.db.commit()

            # Get message ID
            self.cursor.execute("SELECT LAST_INSERT_ID() as id")
            message_id = self.cursor.fetchone()['id']

            # If receiver is online, send message
            if receiver_id in self.clients:
                await self.clients[receiver_id].send(json.dumps({
                    'type': 'message',
                    'sender_id': sender_id,
                    'message': message,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'message_id': message_id
                }))

            return message_id
        except Exception as e:
            print(f"Error sending message: {e}")
            return None

    async def get_chat_history(self, user1_id, user2_id):
        try:
            self.cursor.execute("""
                SELECT m.*, u.name as sender_name
                FROM Messages m
                JOIN users u ON m.sender_id = u.id
                WHERE (m.sender_id = %s AND m.receiver_id = %s)
                OR (m.sender_id = %s AND m.receiver_id = %s)
                ORDER BY m.timestamp ASC
            """, (user1_id, user2_id, user2_id, user1_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []

    async def get_friends(self, user_id):
        try:
            self.cursor.execute("""
                SELECT u.id, u.name, p.profile_picture,
                       (SELECT message FROM Messages 
                        WHERE (sender_id = %s AND receiver_id = u.id)
                        OR (sender_id = u.id AND receiver_id = %s)
                        ORDER BY timestamp DESC LIMIT 1) as last_message,
                       (SELECT timestamp FROM Messages 
                        WHERE (sender_id = %s AND receiver_id = u.id)
                        OR (sender_id = u.id AND receiver_id = %s)
                        ORDER BY timestamp DESC LIMIT 1) as last_message_time
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE u.id IN (
                    SELECT CASE 
                        WHEN user1_id = %s THEN user2_id
                        WHEN user2_id = %s THEN user1_id
                    END
                    FROM friends
                    WHERE user1_id = %s OR user2_id = %s
                )
                ORDER BY last_message_time DESC
            """, (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting friends: {e}")
            return []

    async def handle_message(self, websocket, message_data):
        try:
            data = json.loads(message_data)
            message_type = data.get('type')

            if message_type == 'register':
                user_id = data.get('user_id')
                await self.register(websocket, user_id)
                # Send friends list
                friends = await self.get_friends(user_id)
                await websocket.send(json.dumps({
                    'type': 'friends_list',
                    'friends': friends
                }))

            elif message_type == 'message':
                sender_id = data.get('sender_id')
                receiver_id = data.get('receiver_id')
                message = data.get('message')
                await self.send_message(sender_id, receiver_id, message)

            elif message_type == 'get_chat_history':
                user1_id = data.get('user1_id')
                user2_id = data.get('user2_id')
                history = await self.get_chat_history(user1_id, user2_id)
                await websocket.send(json.dumps({
                    'type': 'chat_history',
                    'history': history
                }))

        except Exception as e:
            print(f"Error handling message: {e}")

    async def handler(self, websocket):
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            # Find and remove disconnected user
            for user_id, ws in self.clients.items():
                if ws == websocket:
                    await self.unregister(user_id)
                    break

async def main():
    server = ChatServer()
    async with websockets.serve(server.handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())