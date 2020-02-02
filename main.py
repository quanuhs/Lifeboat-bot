from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
import vk_api
import random
import time
import sqlite3 as sql
import json

from keyboards import *

# Ключи авторизации.
token = "6bc9bbcee6d582876909b52dbc5c2a68d5334250aecb3250ece8d27f894dde5793dd69f1aa594aa3b3550"
group_id = '191532694'


vk = vk_api.VkApi(token=token)
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, group_id)



def msg(user_id, text):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": text,
               "random_id": 0})


def msg_k(user_id, the_keyboard, text):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": text,
               "keyboard": the_keyboard,
               "random_id": 0})


def is_user_in_game(user_id):
    return False

def any_lobby(user_id):
    print("any")

def enter_code(user_id):
    print("enter_code")

def set_status(user_id, status):
    print("status_changed to:" + str(status))

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = (event.object.from_id)  # Получаем id пользователя.
                request = event.object.text.lower()  # Обробатываем сообщение от пользователя.
                payload = event.object.get("payload")

                if not is_user_in_game(user_id):
                    if payload == "\"create\"":
                        set_status(user_id, "creating_lobby")
                        msg(user_id, "creating")

                    elif payload == "\"main\"":
                        set_status(user_id, "main")
                        msg_k(user_id, two_keyboard("Присоединиться к игре", "primary", "join", "Создать лобби", "secondary", "create"),
                              "Выберите действие: \n1. Присоединиться к созданному лобби. \n2. Создать лобби для игры.")

                    if payload == "\"join\"":
                        set_status(user_id, "join")

                        msg_k(user_id, two_one_keyboard("Случайное лобби", "positive", "any", "Ввести код", "primary", "enter_code", "Вернуться в главное меню", "negative", "main"),
                              "Выберите действие: \n1. Присоединиться к случайному лобби. \n2. Присоединиться к конкретному лобби.")

                    if payload == "\"any\"":
                        set_status(user_id, "lobby_search")
                        any_lobby(user_id)

                    elif payload == "\"enter_code\"":
                        set_status(user_id, "enter_code")
                        msg(user_id, "Пожалуйста напишите секретный код для подключения к лобби:")


                else:
                    print("NOPE")
                    break


    except Exception as e:
        print("Error")
        time.sleep(1)