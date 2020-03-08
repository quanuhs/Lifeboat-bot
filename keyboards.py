import json
from sql_commands import *
from cards_logic import *

import sqlite3 as sql


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


def inline_one(text1, color1, payload1):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(text1, color1, payload1)]
                    ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def inline_two(text1, color1, payload1, text2, color2, payload2):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(text1, color1, payload1)],
            [get_button(text2, color2, payload2)]
                    ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

def inline_three(text1, color1, payload1, text2, color2, payload2, text3, color3, payload3):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(text1, color1, payload1)],
            [get_button(text2, color2, payload2)],
            [get_button(text3, color3, payload3)]
                    ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

def all_players_vote(lobby_id, additional_param):
    users_arr = get_user_info("Lobby_ID", lobby_id)
    players_buttons_arr = []
    for i in range(len(users_arr)):
        players_buttons_arr.append([get_button(str(users_arr[i][3]), "secondary", str(additional_param) + "*" + str(users_arr[i][0]))])

    players_buttons_arr.append([get_button("Отмена", "negative", "game_menu")])

    keyboard = {
        "inline": False,
        "one_time": False,
        "buttons": players_buttons_arr

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
def loot_choice_keyboard(user_id, amount):

    user = get_user_info("User_ID", user_id)
    cards = []
    items = []

    for i in range(amount):
        num = get_lobby_loot_card(user[0][2], i)
        cards.append(get_card_by_type_number("loot", int(num)))
        items.append([cards[i][0], "primary", "lootchoice_"+str(num)])

    if len(items) < 8:
        while len(items) != 8:
            items.append(["---", "primary", ""])

    keybo = items_list_keyboard(items, [], False)
    return keybo


def inventory_list(user_id, page):
    user = get_user_info("User_ID", user_id)

    cards_closed = split_cards(user[0][10])
    cards_active = split_cards(user[0][9])
    cards_open = split_cards(user[0][8])

    sum_cards = len(cards_active) + len(cards_open) + len(cards_closed)

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

    for i in range(page*8, page*8+8):
        if i - len(cards_active) < 0:
            color = "negative"
        elif i - len(cards_active) - len(cards_open) < 0:
            color = "positive"
        else:
            color = "primary"

        if i >= sum_cards and sum_cards%8 != 0:
            items.append(["---", "primary", ""])
        else:
            items.append([cards[i][0], color, "lootcard_"+cards_index[i]])


    if page*8 - sum_cards +8 >= 0:
        page = -1

    extro = get_button("Назад", "secondary", "loot_" + str(page+1)), get_button("Вперёд ", "secondary", "loot_" + str(page+1))

    keybo = items_list_keyboard(items, extro, True)
    return keybo


def items_list_keyboard(items, extra, inline):
    b = [[get_button(items[0][0], items[0][1], items[0][2]), get_button(items[1][0], items[1][1], items[1][2])],
         [get_button(items[2][0], items[2][1], items[2][2]), get_button(items[3][0], items[3][1], items[3][2])],
         [get_button(items[4][0], items[4][1], items[4][2]), get_button(items[5][0], items[5][1], items[5][2])],
         [get_button(items[6][0], items[6][1], items[6][2]), get_button(items[7][0], items[7][1], items[7][2])]]

    if len(extra) != 0:
        b.append(extra)

    keyboard = {
                "inline": inline,
                "one_time": False,
                "buttons": b

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
            [get_button("❤: " + str(HP), "secondary", "HP"), get_button("💪: " + str(Strength), "secondary", "Strength"),
             get_button("🥊: " + str(Fight_Points), "secondary", "Fight_Points"), get_button("🚣: " + str(Row_Points), "secondary", "Row_Points")],
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
