from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
import vk_api
import random
import time
import sqlite3 as sql
import json
import random
import os
import psycopg2

# Ключи авторизации.
token = os.environ.get('key')
group_id = os.environ.get('group_id')
DATABASE_URL = os.environ['DATABASE_URL']

vk = vk_api.VkApi(token=token)
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, group_id)

MAX_PLAYERS = 6
MAX_LOBBIES = 10

try:
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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


def get_card_by_type_number(type, number):
    try:
        connection = sql.connect("cards.db", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM %s" % type)
        result = q.fetchall()
        return result[number]
    except Exception as e:
        print("'get_card_by_type_number'  %s | %s" % (str(type), str(number)))
        return " "


def get_all_type_cards(name):
    try:
        connection = sql.connect("cards.db", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM %s" % name)
        result = q.fetchall()
        connection.close()
        loot = ""
        for i in range(len(result)):
            loot = loot + str(i) + ";"
        loot = loot[:-1]
        return loot
    except Exception as e:
        msg(137155471, "Erorr")
        print("EXP")


def make_cards(cards_array):
    cards = ""
    for i in range(len(cards_array)):
        cards = cards + cards_array[i] + ";"
    cards = cards[:-1]
    return cards


def shake_cards(cards):
    try:
        cards = cards.split(";")
        for i in range(len(cards)):
            first = cards[i]
            random_number = random.randint(0, len(cards) - 1)
            second = cards[random_number]
            cards[i] = second
            cards[random_number] = first
        return make_cards(cards)
    except Exception as e:
        print("Error in shake_cards")


def set_user_info(param, user_id, value):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        q = connection.cursor()
        q.execute(
            "UPDATE user_info SET %s = '%s' WHERE User_ID = %s" % (param, value, user_id))
        connection.commit()
        connection.close()
        print(str(user_id) + " | " + str(param) + " to: " + str(value))

    except Exception as e:
        print("Error in 'set_user_info'")


def get_user_info(param, value):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        q = connection.cursor()
        q.execute("SELECT * FROM user_info WHERE %s = %s" % (param, value))
        result = q.fetchall()
        connection.commit()
        connection.close()
        return result

    except Exception as e:
        print("Error in 'get_user_info'")


def set_status(user_id, status):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        q = connection.cursor()
        q.execute(
            "UPDATE user_info SET Status = '%s' WHERE User_ID = '%s'" % (status, user_id))
        connection.commit()
        connection.close()
        print(str(user_id) + " | status_changed to: " + str(status))
    except Exception as e:
        print("Error in 'set_status'")


def delete_lobby(lobby_id):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        q = connection.cursor()
        q.execute("DELETE FROM lobby_info WHERE Lobby_ID = '%s'" % (lobby_id))
        connection.commit()
        connection.close()

    except Exception as e:
        print("Error in 'delete lobby'")


def get_lobby_info(param, value):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        q = connection.cursor()
        q.execute("SELECT * FROM lobby_info WHERE %s = %s" % (param, value))
        result = q.fetchall()
        connection.commit()
        connection.close()
        return result

    except Exception as e:
        print("Error in 'get_user_info'")


def set_lobby_info(param, lobby_id, value):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        q = connection.cursor()
        q.execute("UPDATE lobby_info SET %s = '%s' WHERE Lobby_ID = %s" % (param, value, lobby_id))
        connection.commit()
        connection.close()
        print(str(lobby_id) + " | " + str(param) + " to: " + str(value))

    except Exception as e:
        print("Error in 'set_lobby_info'")


def change_player_amount(lobby_id, add_number):
    set_lobby_info("Players", lobby_id, get_lobby_info("Lobby_ID", lobby_id)[0][2] + add_number)


def get_button(label, color, payload):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def two_keyboard(text1, color1, payload1, text2, color2, payload2):
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(text1, color1, payload1)],
            [get_button(text2, color2, payload2)]
        ]

    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def card_keyboard():
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button("Припасы", "primary", "loot_0")],
            [get_button("Друг", "positive", "friend"), get_button("Враг", "negative", "enemy")]

        ]

    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def get_card_by_type_number(type, number):
    try:
        connection = sql.connect("cards.db", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM %s" % type)
        result = q.fetchall()
        return result[number]
    except Exception as e:
        print("'get_card_by_type_number'  %s | %s" % (str(type), str(number)))
        return " "


def items_list(user_id, page):
    user = get_user_info("User_ID", user_id)
    cards_closed = str(user[0][10])
    cards_open = str(user[0][8])
    cards_active = str(user[0][9])

    if cards_closed.__contains__(";"):
        cards_closed = cards_closed.split(";")

    if cards_open.__contains__(";"):
        cards_open = cards_open.split(";")

    if cards_active.__contains__(";"):
        cards_active = cards_active.split(";")

    sum_cards = len(cards_active) + len(cards_open) + len(cards_closed)

    if sum_cards % 8 != 0:
        sum_cards = sum_cards + 1

    cards = []
    cards_index = []
    for i in range(len(cards_active)):
        cards.append(get_card_by_type_number("loot", int(cards_active[i])))
        cards_index.append(cards_active[i])

    for i in range(len(cards_open)):
        cards.append(get_card_by_type_number("loot", int(cards_open[i])))
        cards_index.append(cards_open[i])

    for i in range(len(cards_closed)):
        cards.append(get_card_by_type_number("loot", int(cards_closed[i])))
        cards_index.append(cards_closed[i])

    items = []

    if len(cards_index) == 0:
        return

    for i in range(page * 8, page * 8 + 8):
        if i - len(cards_active) < 0:
            color = "negative"
            name = "active_"
        elif i - len(cards_active) - len(cards_open) < 0:
            color = "positive"
            name = "opened_"
        else:
            color = "primary"
            name = "closed_"

        if i >= sum_cards - 1:
            items.append(["---", "primary", ""])
        else:
            items.append([cards[i][0], color, name + cards_index[i]])

    name = "На страницу: [%s]" % (page + 2)
    if page * 8 - sum_cards + 8 >= 0:
        page = -1
        name = "На страницу: [1]"

    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(items[0][0], items[0][1], items[0][2]), get_button(items[1][0], items[1][1], items[1][2])],
            [get_button(items[2][0], items[2][1], items[2][2]), get_button(items[3][0], items[3][1], items[3][2])],
            [get_button(items[4][0], items[4][1], items[4][2]), get_button(items[5][0], items[5][1], items[5][2])],
            [get_button(items[6][0], items[6][1], items[6][2]), get_button(items[7][0], items[7][1], items[7][2])],
            [get_button(name, "secondary", "loot_" + str(page + 1))]
            ]

    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def game_keyboard(user_id):
    user = get_user_info("User_ID", user_id)
    HP = user[0][4]
    Strength = user[0][14]
    Fight_Points = user[0][6]
    Row_Points = user[0][5]

    keyboard = {
        "inline": False,
        "buttons": [
            [get_button("❤: " + str(HP), "secondary", ""), get_button("💪: " + str(Strength), "secondary", ""),
             get_button("🥊: " + str(Fight_Points), "secondary", ""),
             get_button("🚣: " + str(Row_Points), "secondary", "")],
            [get_button("Действия", "primary", "action"), get_button("Карты", "primary", "cards")]

        ]

    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def two_one_keyboard(text1, color1, payload1, text2, color2, payload2, text3, color3, payload3):
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(text1, color1, payload1), get_button(text2, color2, payload2)],
            [get_button(text3, color3, payload3)]
        ]

    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def three_keyboard(text1, color1, payload1, text2, color2, payload2, text3, color3, payload3):
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(text1, color1, payload1)],
            [get_button(text2, color2, payload2)],
            [get_button(text3, color3, payload3)]
        ]

    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


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
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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
    msg_all(lobby_id, "@id" + str(user_id) + " (Пользователь) присоединился к лобби.")
    change_player_amount(lobby_id, 1)
    set_user_info("Lobby_ID", user_id, lobby_id)
    set_status(user_id, "in_game")
    msg_k(user_id,
          two_keyboard("Проголосовать за старт игры", "positive", "vote_game", "Покинуть игровое лобби", "negative",
                       "leave_lobby"), "Вы присоединились к лобби с ID: %s." % lobby_id, )


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
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    q = connection.cursor()
    lobby_id = random.randint(1, 9999999)
    q.execute("SELECT * FROM lobby_info")
    result = q.fetchall()
    if len(result) < MAX_LOBBIES:
        while len(get_lobby_info("Lobby_ID", lobby_id)) != 0:
            lobby_id = random.randint(1, 9999999)

        q.execute(
            "INSERT INTO lobby_info (Lobby_ID, Is_Public, Players, Loot_Cards, Navigation_Cards, Weather_Cards, Players_ID, Status, Votes, Weather, Move)"
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % (
            lobby_id, is_public, 0, shake_cards(get_all_type_cards("loot")),
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
    set_user_info("Cards_Closed", user_id, "")


# Cards_Logic
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
        lobby_cards = get_lobby_info("Lobby_ID", lobby_id)[0][3].replace(chosen_card + ";", "", 1)
    else:
        lobby_cards = get_lobby_info("Lobby_ID", lobby_id)[0][3].replace(";" + chosen_card+";", ";")

    set_lobby_info("Loot_Cards", lobby_id, lobby_cards)
    set_user_info("Cards_Closed", user_id, user_closed_cards)

def open_user_card(user_id, card_number):
    user = get_user_info("User_ID", user_id)
    closed_cards = user[0][10]
    open_cards = user[0][8]
    closed_cards = str(closed_cards).split(";")
    print(closed_cards)
    for i in range(len(closed_cards)):
        if card_number == closed_cards[i]:
            closed_cards.pop(i)
            break
    closed_cards = make_cards(closed_cards)
    print(closed_cards)
    if open_cards != "":
        open_cards = open_cards + ";"+str(card_number)
    else:
        open_cards = open_cards + str(card_number)

    set_user_info("Cards_Open", user_id, open_cards)
    set_user_info("Cards_Closed", user_id, closed_cards)


def loot_cards_choice(lobby, user):
    choice = ""
    for i in range(lobby[0][2] - user[0][11]):
        card = get_lobby_loot_card(lobby[0][0], i)
        card = get_card_by_type_number("loot", int(card))
        choice = choice + str(i + 1) + ". %s\n" % (card[0])
    msg(user_id, choice)


# Cards Logic

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
                               "\nОчков за выживание: %s." % (card[0], card[1], card[2]), card[3])
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
        msg_k(users[i][0], game_keyboard(users[i][0]),
              get_player(users[i][0], "friend") + "\n\n" + get_player(users[i][0], "enemy"))


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
        return "💖 Мой друг: %s.\n________\n💪| Сила: %s.\n💜| Здоровье: %s. \n✨| Очков за выживание: %s." % (
        my_friend[0][3], my_friend[0][14], my_friend[0][4], friend_card[0][2])
    if str(type).lower() == "enemy":
        return "💔 Мой враг: %s.\n________\n💪| Сила: %s.\n🖤| Здоровье: %s. \n⚰| Очков за смерть: %s." % (
        my_enemy[0][3], my_enemy[0][14], my_enemy[0][4], enemy_card[0][1])
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
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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

                connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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

                            msg_k(user_id,
                                  two_one_keyboard("Случайное лобби", "positive", "any", "Ввести код", "primary",
                                                   "enter_code", "Вернуться в главное меню", "negative", "main"),
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
                            number = str(request).replace("!give", "").replace(" ", "")
                            give_user_card(user_id, int(number) - 1)

                        elif request == "!choice":
                            loot_cards_choice(lobby, user)

                        elif payload == "\"vote_game\"":
                            if not lobby[0][6].__contains__(str(user_id) + ";"):
                                set_lobby_info("Votes", lobby[0][0], lobby[0][8] + 1)
                                set_lobby_info("Players_ID", lobby[0][0], lobby[0][6] + str(user_id) + ";")
                                if lobby[0][2] - lobby[0][8] - 1 > 0:
                                    msg_k(user_id, two_keyboard("Отменить голос", "secondary", "vote_game",
                                                                "Покинуть игровое лобби", "negative", "leave_lobby"),
                                          "Вы проголосовали за начало игры.")
                                    msg_all(lobby[0][0],
                                            "До старта осталось голосов: %s." % (lobby[0][2] - lobby[0][8] - 1))
                                else:
                                    game(lobby)

                            else:
                                set_lobby_info("Votes", lobby[0][0], lobby[0][8] - 1)
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
                            msg_k(user_id, items_list(user_id, page), "Страница: [" + str(
                                page + 1) + "]\n\nКрасные - активированные. \nЗелёные - открытые.\n (Если пусто, значит припасов, у вас, нет)")

                        elif str(payload).startswith("\"closed_"):
                            card_n = str(payload).split("_")[1].replace("\"", "")
                            card = get_card_by_type_number("loot", int(card_n))
                            open_user_card(user_id, card_n)
                            
                        break


    except Exception as e:
        print("Error")
        msg(137155471, "Error")
        time.sleep(1)
