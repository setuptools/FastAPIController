from aiogram import Dispatcher , Bot
from aiogram.filters import Command
from aiogram.types import Message

import asyncio

import redis
from redis.asyncio import Redis
import json

class SampleBot(Bot):
    dp = Dispatcher()

    def __init__(self, token):
        super(SampleBot , self).__init__(token)

        print("It's a sample bot")
        asyncio.create_task(self.sendUsersToRedis())

        @self.dp.message(Command("start"))
        async def welcome(message:Message = None):
            await self.send_message(message.chat.id ,"Hello world , it's a test message!")
            print(message.from_user.id)
        
        asyncio.create_task(self.listenRedis())
    
    async def listenRedis(self):
        redis = Redis.from_url("redis://localhost:6379", decode_responses=True)
        pubsub = redis.pubsub()
        await pubsub.subscribe("bot_messaging", "bot_user_ids", "bot_urls")
        print("Подключено к каналу 'bot_messaging'&'bot_user_ids'")

        _message = None
        _urls = None

        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"]
                print(f"Получено сообщение: {data}")
                
                if message["channel"] == "bot_messaging":
                    _message = message["data"]
                
                elif message["channel"] == "bot_urls":
                    _urls = message["data"]

                # Пример: отправка сообщения в Telegram
                try:
                    if message["channel"] == "bot_user_ids":
                        users_ids = data.split(",")

                        for user in users_ids:
                            user = user.replace('"',"")
                            await self.send_message(chat_id=int(user), text=_message)
                        
                        _message = None

                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")
    
    async def sendUsersToRedis(self):
        # set host and port than set in redis-server
        redi = await Redis(host = "127.0.0.1", port = "6379",decode_responses= True)
        
        users_data = [] #There your users id

        await redi.publish("user_ids", ",".join( str(x) for x in users_data))
    

if __name__ == "__main__":
    async def main():
        bot = SampleBot(token = "YOUR TOKEN HERE")

        await SampleBot.dp.start_polling(bot)
    
    asyncio.run(main())