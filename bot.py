# Tic Tac Toe
from configparser import ConfigParser
import requests
import json


class Bot:
    def __init__(self, path):
        TOKEN = self.get_telegram_token(path)
        self.photo_id = self.get_telegram_photo_id(path)
        self.phone_num = self.get_phone_num(path)
        self.url_base = "https://api.telegram.org/bot" + TOKEN

        self.initial_buttons = self.load_board()

        self.current_message_id = 0
        self.last_stored_message_id = 0
        self.my_symbol = ""
        self.opponent_symbol = ""
        self.STATUS = "start"

    def get_telegram_token(self, path):
        config = ConfigParser()
        config.read(path)
        token = config['creds']['token']
        return token

    def get_telegram_photo_id(self, path):
        config = ConfigParser()
        config.read(path)
        photo_id = config['creds']['photo_id']
        return photo_id

    def get_phone_num(self, path):
        config = ConfigParser()
        config.read(path)
        photo_id = config['creds']['phone_num']
        return photo_id

    def get_messages(self):
        url = self.url_base + "/getUpdates"
        res = requests.get(url)

    def load_board(self):
        with open('buttons.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    def check_if_button(self, message):
        if 'callback_query' in message:
            print(True)
            return True
        else:
            print(False)
            return False

    def parse_button(self, message):
        chat_id = message['callback_query']['message']['chat']['id']
        message_id = message['callback_query']['message']['message_id']
        data = message['callback_query']['data']
        return chat_id, message_id, data

    def parse_message(self, message_recieved):
        error_return_value = {
            "message_type": "000",
            "chat_id": "000",
            "message_id": "000",
            "data": "000",
            "time": "000"
        }

        try:
            if 'message' in message_recieved and not 'photo' in message_recieved['message']:
                message_type = 'message'
                chat_id = message_recieved['message']['chat']['id']
                message_id = message_recieved['message']['message_id']
                if 'text' in message_recieved['message']:
                    data = message_recieved['message']['text']
                elif 'dice' in message_recieved['message']:
                    message_type = 'dice'
                    data = message_recieved['message']['dice']['value']
                if 'entities' in message_recieved['message'] \
                        and message_recieved['message']['entities'][0]['type'] == 'bot_command':
                    message_type = 'command'
                time = message_recieved['message']['date']
            elif 'edited_message' in message_recieved:
                message_type = 'edited_message'
                chat_id = message_recieved['edited_message']['chat']['id']
                message_id = message_recieved['edited_message']['message_id']
                data = message_recieved['edited_message']['text']
                time = message_recieved['message']['date']
            elif 'callback_query' in message_recieved:
                message_type = 'button'
                chat_id = message_recieved['callback_query']['message']['chat']['id']
                message_id = message_recieved['callback_query']['message']['message_id']
                data = message_recieved['callback_query']['data']
                time = message_recieved['callback_query']['message']['date']
            elif 'photo' in message_recieved['message']:
                message_type = 'photo'
                chat_id = message_recieved['message']['chat']['id']
                message_id = message_recieved['message']['message_id']
                data = message_recieved['message']['photo'][0]['file_id']
                time = message_recieved['message']['date']


        except KeyError:
            return error_return_value
        else:
            try:
                return {
                    "message_type": message_type,
                    "chat_id": str(chat_id),
                    "message_id": message_id,
                    "data": data,
                    "time": time
                }
            except UnboundLocalError:
                return error_return_value

    def is_message_command(self, message):
        try:
            if 'entities' in message['message']:
                if message['message']['entities'][0]['type'] == 'bot_command':
                    return True
            else:
                return False
        except KeyError:
            return False

    def parse_command(self, text):
        if text == '/start':
            print("asdasdasd")

    def send_message(self, chat_id, text):
        url = self.url_base + "/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        res = requests.post(url, data=payload)
        res = res.json()
        if res['ok'] != True:
            raise Exception

    def send_contact(self, chat_id):
        url = self.url_base + "/sendContact"
        payload = {"chat_id": chat_id, "phone_number": self.phone_num,
                   "first_name": "Niv"}
        res = requests.post(url, data=payload)
        res = res.json()

    def button(self, chat_id, message, json_buttons):
        url = self.url_base + "/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        initial_buttons = self.initial_buttons
        buttons = {"reply_markup": json_buttons}
        payload.update(buttons)
        res = requests.post(url, json=payload)

    def get_button_pressed(self, press_data):
        button_pressed = press_data.split("-")
        button_pressed = tuple(map(lambda x: int(x), button_pressed))
        return button_pressed

    def edit_button(self, chat_id, message_id, button_pressed, symbol):
        url = self.url_base + "/editMessageReplyMarkup"
        payload = {"chat_id": chat_id, "message_id": message_id}
        initial_buttons = self.initial_buttons['Game']
        initial_buttons['inline_keyboard'][button_pressed[1]][button_pressed[0]]['text'] = symbol
        inline_keyboard = {"reply_markup": initial_buttons}
        payload.update(inline_keyboard)
        res = requests.post(url, json=payload)
        return res.json()

    def delete_button(self, chat_id, message):
        url = self.url_base + "/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        keyboard = {"reply_markup": {"remove_keyboard": True}}
        payload.update(keyboard)
        res = requests.post(url, json=payload)

    def send_chat_action(self, chat_id):
        url = self.url_base + "/sendChatAction"
        payload = {"chat_id": chat_id, "action": "typing"}
        res = requests.post(url, json=payload)

    def send_dice(self, chat_id):
        url = self.url_base + "/sendDice"
        payload = {"chat_id": chat_id, "emoji": "🎲"}
        res = requests.post(url, json=payload)

    def send_photo(self, chat_id, message_id):
        url = self.url_base + "/sendPhoto"
        # my photo id is attached from the telegram servers
        payload = {"chat_id": chat_id,
                   "photo": self.photo_id,
                   "reply_to_message_id": message_id}
        res = requests.post(url, json=payload)
