import sqlite3 as sql

def set_user_info(param, user_id, value):
    try:
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute(
            "UPDATE user_info SET %s = '%s' WHERE User_ID = '%s'" % (param, value, user_id))
        connection.commit()
        connection.close()
        print(str(user_id) + " | " + str(param) + " to: " + str(value))

    except Exception as e:
        print("Error in 'set_user_info'")


def get_user_info(param, value):
    try:
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
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
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
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
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("DELETE FROM lobby_info WHERE Lobby_ID = '%s'" % (lobby_id))
        connection.commit()
        connection.close()

    except Exception as e:
        print("Error in 'delete lobby'")



def get_lobby_info(param, value):
    try:
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
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
        connection = sql.connect("lifeboat.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("UPDATE lobby_info SET %s = '%s' WHERE Lobby_ID = %s" % (param, value, lobby_id))
        connection.commit()
        connection.close()
        print(str(lobby_id) + " | " + str(param) + " to: " + str(value))

    except Exception as e:
        print("Error in 'set_lobby_info'")



def change_player_amount(lobby_id, add_number):
    set_lobby_info("Players", lobby_id, get_lobby_info("Lobby_ID", lobby_id)[0][2] + add_number)

