from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
import vk_api

import sqlite3 as sql
import json


connection = sql.connect("cards.db", check_same_thread=False)
q = connection.cursor()
q.execute("SELECT * FROM cards")
result = q.fetchall()
for i in range(len(result)):
    print(result[i])

print(str(len(result)))