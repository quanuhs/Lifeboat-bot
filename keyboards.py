import json

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
