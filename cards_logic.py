from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
import vk_api

import sqlite3 as sql
import random
import json
from sql_commands import *


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

def get_lobby_loot_card(lobby_id, position):
    lobby_cards = get_lobby_info("Lobby_ID", lobby_id)[0][3].split(";")
    return lobby_cards[position]


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
        print("EXP")


def make_cards(cards_array):
    cards = ""
    for i in range(len(cards_array)):
        cards = cards + cards_array[i] + ";"
    cards = cards[:-1]
    return cards


def split_cards(card_line):
    if card_line.__contains__(";"):
        cards_a = card_line.split(";")
    elif card_line.isnumeric():
        cards_a = [card_line]
    else:
        cards_a = []

    return cards_a


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
