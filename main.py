from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
import vk_api
import random
import time
import sqlite3 as sql
import json
import random
import os
import psycopg2

from keyboards import *
from sql_commands import *
from cards_logic import *

# Ключи авторизации.
token = "6bc9bbcee6d582876909b52dbc5c2a68d5334250aecb3250ece8d27f894dde5793dd69f1aa594aa3b3550"
group_id = '191532694'

#DATABASE_URL = os.environ['DATABASE_URL']
vk = vk_api.VkApi(token=token)
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, group_id)


MAX_PLAYERS = 6
MAX_LOBBIES = 10

try:
    #connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
    q = connection.cursor()

    q.execute('''CREATE TABLE user_info
        (
        User_ID INTEGER,
        Status TEXT,
        Lobby_ID INTEGER,
        Role TEXT,
        HP INTEGER,
        Thirst_Points INTEGER,
        Fight_Points INTEGER,
        Fight_Player INTEGER,
        Cards_Open TEXT,
        Cards_Activated TEXT,
        Cards_Closed TEXT,
        Position INTEGER,
        Friend TEXT,
        Enemy TEXT,
        Strength INTEGER
        )
        ''')

    q.execute('''CREATE TABLE lobby_info
        (
        Lobby_ID INTEGER,
        Is_Public BOOLEAN,
        Players INTEGER,
        Loot_Cards TEXT,
        Navigation_Cards TEXT,
        Weather_Cards TEXT,
        Players_ID TEXT,
        Status TEXT,
        Votes INTEGER,
        Weather INTEGER,
        Move INTEGER
        
        )
        ''')


    q.close()
    connection.commit()
    connection.close()
    print("Создаём базу.")
except Exception as E:
    print("База уже создана.")

def msg(user_id, text):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": text,
               "random_id": 0})

def msg_photo(user_id, text, photo):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": text,
               "attachment": photo,
               "random_id": 0})

def msg_k(user_id, the_keyboard, text):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": text,
               "keyboard": the_keyboard,
               "random_id": 0})

def is_user_in_game(user_id):
    res = False
    try:
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM user_info WHERE User_ID = '%s'" % (user_id))
        result = q.fetchall()
        if result[0][1] == "in_game" and not result[0][2] == -1:
            res = True

        connection.close()
    except Exception as e:
        print("Error in 'is_user_in_game'")

    return res

def any_lobby(user_id):
    try:
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM lobby_info WHERE Is_Public = '%s' AND Players < '%s'" % (True, MAX_PLAYERS))
        result = q.fetchall()
        if len(result) == 0:
            create_lobby(user_id, True)
            q.execute("SELECT * FROM lobby_info WHERE Is_Public = '%s' AND Players < '%s'" % (True, MAX_PLAYERS))
            result = q.fetchall()

        join_lobby(user_id, result[0][0])

        connection.close()
    except Exception as e:
        print("Error in any_lobby")

def join_lobby(user_id, lobby_id):
    msg_all(lobby_id, "@id"+str(user_id)+" (Пользователь) присоединился к лобби.")
    change_player_amount(lobby_id, 1)
    set_user_info("Lobby_ID", user_id, lobby_id)
    set_status(user_id, "in_game")
    msg_k(user_id,
        two_keyboard("Проголосовать за старт игры", "positive", "vote_game", "Покинуть игровое лобби", "negative", "leave_lobby"), "Вы присоединились к лобби с ID: %s." %lobby_id,)

def enter_code(user_id):
    print("enter_code")

def leave_lobby(user_id):
    lobby_id = get_user_info("User_ID", user_id)[0][2]
    set_user_info("Lobby_ID", user_id, -1)
    change_player_amount(lobby_id, -1)
    msg_all(lobby_id, "@id" + str(user_id) + " (Пользователь) покинул лобби.")
    if get_lobby_info("Lobby_ID", lobby_id)[0][2] == 0:
        delete_lobby(lobby_id)


def create_lobby(user_id, is_public):
    connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
    q = connection.cursor()
    lobby_id = random.randint(1, 9999999)
    q.execute("SELECT * FROM lobby_info")
    result = q.fetchall()
    if len(result) < MAX_LOBBIES:
        while len(get_lobby_info("Lobby_ID", lobby_id)) != 0:
            lobby_id = random.randint(1, 9999999)

        q.execute("INSERT INTO lobby_info (Lobby_ID, Is_Public, Players, Loot_Cards, Navigation_Cards, Weather_Cards, Players_ID, Status, Votes, Weather, Move)"
                      "VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % (lobby_id, is_public, 0, shake_cards(get_all_type_cards("loot")),
                                                                       shake_cards(get_all_type_cards("navigation")), "", "", "", 0, -1, 0))

        connection.commit()

        if not is_public:
            msg(user_id, "Лобби было создано. Его ID (код): " + str(lobby_id))
            join_lobby(user_id, lobby_id)

    else:
        msg(user_id, "К сожалению, сейчас вы не можете создать лобби.")

    connection.close()

def main_menu(user_id):
    set_status(user_id, "main")
    msg_k(user_id, two_keyboard("Присоединиться к игре", "primary", "join", "Создать лобби", "secondary", "create"),
          "Выберите действие: \n1. Присоединиться к созданному лобби. \n2. Создать лобби для игры.")

def clear_user(user_id):
    set_user_info("Role", user_id, "")
    set_user_info("HP", user_id, 0)
    set_user_info("Thirst_Points", user_id, 0)
    set_user_info("Fight_Points", user_id, 0)
    set_user_info("Fight_Player", user_id, -1)
    set_user_info("Cards_Open", user_id, "")
    set_user_info("Cards_Activated", user_id, "")
    set_user_info   ("Cards_Closed", user_id, "")

#Cards_Logic
def get_lobby_loot_card(lobby_id, position):
    lobby_cards = get_lobby_info("Lobby_ID", lobby_id)[0][3].split(";")
    return lobby_cards[position]

def give_user_card(user_id, position):
    lobby_id = get_user_info("User_ID", user_id)[0][2]
    chosen_card = get_lobby_loot_card(lobby_id, position)
    user_closed_cards = get_user_info("User_ID", user_id)[0][10]
    if user_closed_cards != "":
        dell =";"
    else:
        dell =""

    user_closed_cards = user_closed_cards + dell + str(chosen_card)
    if position == 0:
        lobby_cards = get_lobby_info("Lobby_ID", lobby_id)[0][3].replace(chosen_card + ";", "")
    else:
        lobby_cards = get_lobby_info("Lobby_ID", lobby_id)[0][3].replace(";" + chosen_card+";", ";")

    set_lobby_info("Loot_Cards", lobby_id, lobby_cards)
    set_user_info("Cards_Closed", user_id, user_closed_cards)


def loot_cards_choice(lobby, user):
    choice = ""
    for i in range(lobby[0][2] - user[0][11]):
        card = get_lobby_loot_card(lobby[0][0], i)
        card = get_card_by_type_number("loot", int(card))
        choice = choice + str(i + 1) + ". %s\n" % (card[0])
    msg(user_id, choice)
#Cards Logic

def msg_all(lobby_id, text):
    users = get_user_info("Lobby_ID", lobby_id)
    for i in range(len(users)):
        msg(users[i][0], text)

def msg_k_all(lobby_id, keyboard, text):
    users = get_user_info("Lobby_ID", lobby_id)
    for i in range(len(users)):
        msg_k(users[i][0], keyboard, text)

def game(lobby):
    set_roles(lobby)


def position(lobby):
    print("ok")

def set_roles(lobby):
    roles = shake_cards(get_all_type_cards("chars")).split(";")
    users = get_user_info("Lobby_ID", lobby[0][0])
    for i in range(lobby[0][2]):
        card = get_card_by_type_number("chars", int(roles[i]))
        msg_photo(users[i][0], "Вы получили роль: '%s'."
                               "\nСила/Здоровье: %s."
                               "\nОчков за выживание: %s." %(card[0], card[1], card[2]), card[3])
        set_user_info("Role", users[i][0], card[0])
        set_user_info("HP", users[i][0], card[1])
        set_user_info("Strength", users[i][0], card[1])

    users = get_user_info("Lobby_ID", lobby[0][0])

    users_roles = ""
    for i in range(lobby[0][2]):
        users_roles = users_roles + users[i][3] + ";"

    users_roles = users_roles[:-1]
    friends = shake_cards(users_roles).split(";")
    enemies = shake_cards(users_roles).split(";")

    for i in range(lobby[0][2]):
        set_user_info("Friend", users[i][0], friends[i])
        set_user_info("Enemy", users[i][0], enemies[i])
        msg_k(user[i][0], game_keyboard(user[i][0]),
              get_player(user[i][0], "friend") + "\n\n" + get_player(user[i][0], "enemy"))

def get_player(user_id, type):
    user = get_user_info("User_ID", user_id)
    my_friend = get_player_info(user[0][12], user[0][2])
    my_enemy = get_player_info(user[0][13], user[0][2])
    connection = sql.connect("cards.db", check_same_thread=False)
    q = connection.cursor()
    friend_card = q.execute("SELECT * FROM chars WHERE Name = '%s'" % user[0][12]).fetchall()
    enemy_card = q.execute("SELECT * FROM chars WHERE Name = '%s'" % user[0][13]).fetchall()
    connection.close()

    if str(type).lower() == "friend":
        return "💖 Мой друг: %s.\n________\n💪| Сила: %s.\n💜| Здоровье: %s. \n✨| Очков за выживание: %s." % (my_friend[0][3], my_friend[0][14], my_friend[0][4], friend_card[0][2])
    if str(type).lower() == "enemy":
        return "💔 Мой враг: %s.\n________\n💪| Сила: %s.\n🖤| Здоровье: %s. \n⚰| Очков за смерть: %s." % (my_enemy[0][3], my_enemy[0][14], my_enemy[0][4], enemy_card[0][1])
    if str(type).lower() == "cards":
        if user[0][10] != "":
            close_cards = user[0][10].split(";")
        else:
            return "У вас нет карт припасов."
        c_cards = "\n\nЗакрытые карты: \n"
        for i in range(len(close_cards)):
            c_cards = c_cards + str(i + 1) + ". " + get_card_by_type_number("loot", int(close_cards[i]))[0] + "\n"
        return "Мои припасы: " + c_cards

def get_player_cards(type):
    print(type)

def get_player_info(role, lobby_id):
    try:
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM user_info WHERE Role = '%s' and Lobby_ID = '%s'" % (role, lobby_id))
        result = q.fetchall()
        connection.commit()
        connection.close()
        return result

    except Exception as e:
        print("Error in 'get_user_info'")

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = (event.object.from_id)  # Получаем id пользователя.
                request = event.object.text.lower()  # Обробатываем сообщение от пользователя.
                payload = event.object.get("payload")

                connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
                q = connection.cursor()
                q.execute("SELECT * FROM user_info WHERE User_ID = '%s'" % (user_id))
                result = q.fetchall()
                if len(result) == 0:
                    q.execute(
                        "INSERT INTO user_info (User_ID, Status, Lobby_ID, Role,"
                        "HP, Thirst_Points, Fight_Points, Fight_Player, "
                        "Cards_Open, Cards_Activated, Cards_Closed, Position, Friend, Enemy, Strength) "
                        "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                            user_id, "main", -1, "", 0, 0, 0, -1, "", "", "", 0, -1, -1, 0))
                    connection.commit()
                    connection.close()
                    msg_k(user_id,
                          two_keyboard("Присоединиться к игре", "primary", "join", "Создать лобби", "secondary",
                                       "create"),
                          "Выберите действие: \n1. Присоединиться к созданному лобби. \n2. Создать лобби для игры.")
                else:
                    if not is_user_in_game(user_id):
                        if payload == "\"create\"":
                            set_status(user_id, "creating_lobby")
                            create_lobby(user_id, False)

                        elif payload == "\"main\"":
                            main_menu(user_id)

                        if payload == "\"join\"":
                            set_status(user_id, "join")

                            msg_k(user_id, two_one_keyboard("Случайное лобби", "positive", "any", "Ввести код", "primary", "enter_code", "Вернуться в главное меню", "negative", "main"),
                                  "Выберите действие: \n1. Присоединиться к случайному лобби. \n2. Присоединиться к конкретному лобби.")

                        if payload == "\"any\"":
                            any_lobby(user_id)


                        elif payload == "\"enter_code\"":
                            set_status(user_id, "enter_code")
                            msg(user_id, "Пожалуйста напишите секретный код для подключения к лобби:")


                    else:

                        user = get_user_info("User_ID", user_id)
                        lobby = get_lobby_info("Lobby_ID", user[0][2])

                        if request == "!test":
                            msg_k(user_id, items_list(user_id, 0), "worked")

                        if payload == "\"leave_lobby\"":
                            leave_lobby(user_id)
                            main_menu(user_id)
                            clear_user(user_id)

                        elif str(request).startswith("!give"):
                            number = str(request).replace("!give", "").replace(" ","")
                            give_user_card(user_id, int(number)-1)

                        elif request == "!choice":
                            loot_cards_choice(lobby, user)

                        elif payload == "\"vote_game\"":
                            if not lobby[0][6].__contains__(str(user_id)+";"):
                                set_lobby_info("Votes", lobby[0][0], lobby[0][8]+1)
                                set_lobby_info("Players_ID", lobby[0][0], lobby[0][6] + str(user_id) + ";")
                                if lobby[0][2] - lobby[0][8] - 1 > 0:
                                    msg_k(user_id, two_keyboard("Отменить голос", "secondary", "vote_game", "Покинуть игровое лобби", "negative", "leave_lobby"),
                                          "Вы проголосовали за начало игры.")
                                    msg_all(lobby[0][0], "До старта осталось голосов: %s." %(lobby[0][2] - lobby[0][8]-1))
                                else:
                                    game(lobby)

                            else:
                                set_lobby_info("Votes", lobby[0][0], lobby[0][8]-1)
                                set_lobby_info("Players_ID", lobby[0][0], lobby[0][6].replace(str(user_id) + ";", ""))
                                msg_k(user_id,
                                      two_keyboard("Проголосовать за старт игры", "positive", "vote_game",
                                                   "Покинуть игровое лобби", "negative", "leave_lobby"),
                                      "Вы отменили свой голос.")
                                msg_all(lobby[0][0],
                                        "До старта осталось голосов: %s." % (lobby[0][2] - lobby[0][8] + 1))

                        elif payload == "\"cards\"":
                            msg_k(user_id, card_keyboard(), "Какие карты вы бы хотели посмотреть?")

                        elif payload == "\"friend\"":
                            msg(user_id, get_player(user_id, "friend"))

                        elif payload == "\"enemy\"":
                            msg(user_id, get_player(user_id, "enemy"))
                        elif str(payload).startswith("\"loot_"):
                            page = int(payload.split("_")[1].replace("\"", ""))
                            msg_k(user_id, items_list(user_id, page), "Страница: [" +str(page+1) + "]\n\nКрасные - активированные. \nЗелёные - открытые.\n (Если пусто, значит припасов, у вас, нет)")

                        elif str(payload).startswith("\"closed_"):
                            card_n = str(payload).split("_")[1].replace("\"", "")
                            card = get_card_by_type_number("loot", int(card_n))
                            if card[1]:
                                msg(user_id, "Вы использовали: " + card[0])
                        break


    except Exception as e:
        print("Error"/0)
        time.sleep(1)