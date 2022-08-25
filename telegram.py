from flask import Flask
from flask import Response

from flask import request
from config import Config

from bot import Bot
from game_flow import Game
import random
import time

from flask_sslify import SSLify

bot = Bot('cfg.ini')
game = Game()
app = Flask(__name__)
sslify = SSLify(app)

config = Config()

emojis = ['\U0001f600', '\U0001f603', '\U0001f604', '\U0001f601', '\U0001f606',
          '\U0001f605', '\U0001f602', '\U0001f923', '\u263a', '\U0001f60a',
          '\U0001f607', '\U0001f642', '\U0001f643', '\U0001f609', '\U0001f60c',
          '\U0001f60d', '\U0001f970', '\U0001f618', '\U0001f617', '\U0001f619',
          '\U0001f61a', '\U0001f60b', '\U0001f61b', '\U0001f61d', '\U0001f61c',
          '\U0001f92a', '\U0001f928', '\U0001f9d0', '\U0001f913', '\U0001f60e',
          '\U0001f929', '\U0001f973', '\U0001f60f', '\U0001f612', '\U0001f61e',
          '\U0001f614', '\U0001f61f', '\U0001f615', '\U0001f641', '\u2639',
          '\U0001f623', '\U0001f616', '\U0001f62b', '\U0001f629', '\U0001f97a',
          '\U0001f622', '\U0001f62d', '\U0001f624', '\U0001f620', '\U0001f621',
          '\U0001f92c', '\U0001f92f', '\U0001f633', '\U0001f975', '\U0001f976',
          '\U0001f631', '\U0001f628', '\U0001f630', '\U0001f625', '\U0001f613',
          '\U0001f917', '\U0001f914', '\U0001f92d', '\U0001f92b', '\U0001f925',
          '\U0001f636', '\U0001f610', '\U0001f611', '\U0001f62c', '\U0001f644',
          '\U0001f62f', '\U0001f626', '\U0001f627', '\U0001f62e', '\U0001f632',
          '\U0001f971', '\U0001f634', '\U0001f924', '\U0001f62a', '\U0001f635',
          '\U0001f910', '\U0001f974', '\U0001f922', '\U0001f92e', '\U0001f927',
          '\U0001f637', '\U0001f912', '\U0001f915', '\U0001f911', '\U0001f920',
          '\U0001f608', '\U0001f47f', '\U0001f479', '\U0001f47a', '\U0001f921',
          '\U0001f4a9', '\U0001f47b', '\U0001f480', '\u2620', '\U0001f47d',
          '\U0001f47e', '\U0001f916', '\U0001f383', '\U0001f63a', '\U0001f638',
          '\U0001f639', '\U0001f63b', '\U0001f63c', '\U0001f63d', '\U0001f640',
          '\U0001f63f', '\U0001f63e']


@app.route("/", methods=['POST', 'GET'])
def home():
    print(config.CACHE)
    if request.method == 'POST':
        msg_recieved = request.get_json()

        parsed_message = bot.parse_message(msg_recieved)
        chat_id = parsed_message['chat_id']
        config.check_cache(chat_id, parsed_message)

        BOT_STATE = config.CACHE[chat_id]['BOT_STATE']
        GAME_SCENE = config.CACHE[chat_id]['GAME_SCENE']
        message_type = config.CACHE[chat_id]['message_type']
        message_id = config.CACHE[chat_id]['message_id']
        data = config.CACHE[chat_id]['data']

        bot.current_message_id = message_id

        if message_type == "command" and data == "/start":
            BOT_STATE = "start"
            GAME_SCENE = 0

        if BOT_STATE == "start" and GAME_SCENE == 0:
            bot.button(chat_id, "Click on a button from the main menu \U0001f447", bot.initial_buttons['Menu'])
            BOT_STATE = "menu"

        # if bot.STATUS == "menu" and game.STATUS == 0:
        if BOT_STATE == "menu" and GAME_SCENE == 0:
            if message_type == "message" and data == "\u274c Tic Tac Toe \u2b55":
                bot.button(chat_id, "Send any symbol or emoji you want or click on one of the buttons",
                           bot.initial_buttons['StartGame'])
                BOT_STATE = "game"
                GAME_SCENE = 1
            elif message_type == "message" and data == "Payments \U0001f4b8":
                # bot.button(chat_id, "The payments section is under experiments \u2699\n"
                #                     "Payments and transfers with crypto currencies might be added soon \U0001f4b1", bot.initial_buttons['Payments'])
                BOT_STATE = "payments"
                bot.send_photo(chat_id, message_id)
                bot.button(chat_id, "\U0001f446 Here is a screenshot of my Binance wallet address.\n"
                                    "You can import it in the Binance app to make transfers \U0001f4b0",
                           bot.initial_buttons['Payments'])


            elif message_type == "message" and data == "Timer \u23f1":
                bot.button(chat_id, "The timer section is available only for Niv!", bot.initial_buttons['Timer'])
                if chat_id == "1205822860":
                    BOT_STATE = "timer"

            elif message_type == "message" and data == "About & Contact \U0001f464":
                bot.button(chat_id, "Hey \U0001f44b \n"
                                    "I am Niv and this is my Telegram bot \n"
                                    "this bot is built with Python and Flask framework.\n"
                                    "Do you want your own bot? \U0001f47e \n"
                                    "Feel free to contact me if you are intersted in: \n"
                                    "\u2705 Bots \U0001f916 \n"
                                    "\u2705 Automations and scripts \U0001f4df \n"
                                    "\u2705 Web scraping and information consumption \U0001f9fe \n"
                                    "\u2705 Or any other thing \U0001f643 \n",
                           bot.initial_buttons['About'])
                BOT_STATE = "about"

        if BOT_STATE == "payments" and GAME_SCENE == 0:
            if message_type == 'button' and data == "Back \U0001f519":
                BOT_STATE = "menu"
                bot.button(chat_id, "Click on a button from the main menu \U0001f447", bot.initial_buttons['Menu'])

        if BOT_STATE == "timer":
            if message_type == "button":
                if data == "start":
                    config.start_timer()
                    bot.send_message(chat_id, "Started timer")
                    BOT_STATE = "timer_on"
                elif data == "Back \U0001f519":
                    BOT_STATE = "menu"
                    bot.button(chat_id, "Click on a button from the main menu \U0001f447", bot.initial_buttons['Menu'])
            if message_type == "message" and data != "Timer \u23f1" and chat_id == "1205822860":
                time_to_send = config.get_times(data)
                bot.send_message(chat_id, time_to_send)

        if BOT_STATE == "timer_on":
            if message_type == "button" and data == "stop":
                total_time = config.stop_timer()
                bot.send_message(chat_id, f"Session took {total_time} seconds")
                BOT_STATE = "timer"

        if BOT_STATE == "about" and GAME_SCENE == 0:
            if message_type == "button":
                if data == "contact":
                    bot.send_message(chat_id, "I'll be happy to hear from you soon \U0001f643")
                    bot.send_contact(chat_id)

                BOT_STATE = "menu"
                bot.button(chat_id, "Click on a button from the main menu \U0001f447", bot.initial_buttons['Menu'])

        if BOT_STATE == "game" and GAME_SCENE == 1:

            if message_type == 'message' and len(data) == 1:
                bot.my_symbol = data
                if data == "\u274c":
                    bot.opponent_symbol = "\u2b55"
                elif data == "\u2b55":
                    bot.opponent_symbol = "\u274c"
                elif data in emojis:
                    emojis.remove(data)
                    bot.opponent_symbol = random.choice(emojis)
                    emojis.append(data)
                else:
                    bot.send_message(chat_id, "This bot does not support this specific symbol, send different emoji...")
                    bot.opponent_symbol = "XXX"

                if bot.opponent_symbol != "XXX":
                    GAME_SCENE = 2

            elif message_type == 'message' and len(data) != 1 and data != "\u274c Tic Tac Toe \u2b55":
                bot.send_message(chat_id,
                                 "The symbol must contain a single character or this bot does not support this specific symbol!")
            else:
                if data != "\u274c Tic Tac Toe \u2b55":
                    bot.send_message(chat_id, "Please send a valid symbol")

        if BOT_STATE == "game" and GAME_SCENE == 2:
            bot.delete_button(chat_id, f"Roll a dice to decide who is gonna take the first move")
            bot.button(chat_id, "But first choose Odd or Even", bot.initial_buttons['OddOrEven'])
            GAME_SCENE = 3

        if BOT_STATE == "game" and GAME_SCENE == 3:
            if message_type == 'message':
                game.odd_or_even = data
                if game.odd_or_even == "Odd \U0001f46a" or game.odd_or_even == "Even \U0001f46c":
                    bot.button(chat_id, "Roll the dice!", bot.initial_buttons['Dice'])
                    GAME_SCENE = 4

        if BOT_STATE == "game" and GAME_SCENE == 4 and message_type == 'dice':
            time.sleep(3.5)
            options = {"Odd \U0001f46a": [1, 3, 5], "Even \U0001f46c": [2, 4, 6]}
            # the data variable is the dice result
            result = data
            if game.odd_or_even in options and result in options[game.odd_or_even]:
                bot.button(chat_id, "You start \U0001f643", bot.initial_buttons['Game'])
                GAME_SCENE = 6
            else:
                bot.button(chat_id, "The bot starts \U0001f916", bot.initial_buttons['Game'])
                bot.last_stored_message_id = message_id
                GAME_SCENE = 5

        if BOT_STATE == "game" and GAME_SCENE == 5:
            opponent_choice = game.get_opponent_choice()
            game.opponent_turn(opponent_choice)
            while not bot.edit_button(chat_id, bot.last_stored_message_id,
                                      opponent_choice, bot.opponent_symbol)['ok']:
                bot.last_stored_message_id += 1
                print(bot.last_stored_message_id)
            GAME_SCENE = 6

        if BOT_STATE == "game" and GAME_SCENE == 6:
            if message_type == 'button':
                choice = bot.get_button_pressed(data)
                if message_id == bot.current_message_id:
                    bot.edit_button(chat_id, message_id, choice, bot.my_symbol)
                    my_turn = game.my_turn(choice)
                    if my_turn != None:
                        GAME_SCENE = 8
                        game.restart()
                        bot.initial_buttons = bot.load_board()
                        if my_turn == "win":
                            bot.send_message(chat_id, "WIN!")
                        elif my_turn == "tie":
                            bot.send_message(chat_id, "TIE!")
                    elif game.check_if_game_ends_in_tie():
                        bot.send_message(chat_id, "TIE!")
                        GAME_SCENE = 8
                        game.restart()
                        bot.initial_buttons = bot.load_board()
                    else:
                        GAME_SCENE = 7

        if BOT_STATE == "game" and GAME_SCENE == 7:
            bot.send_chat_action(chat_id)
            opponent_choice = game.get_opponent_choice()
            opponent_turn = game.opponent_turn(opponent_choice)
            try:
                bot.edit_button(chat_id, message_id, opponent_choice, bot.opponent_symbol)
            except TypeError:
                pass
            if game.check_if_game_ends_in_tie():
                bot.send_message(chat_id, "TIE!")
                GAME_SCENE = 8
                game.restart()
                bot.initial_buttons = bot.load_board()
            elif opponent_turn == "lose":
                bot.send_message(chat_id, "LOSE!")
                GAME_SCENE = 8
                game.restart()
                bot.initial_buttons = bot.load_board()
            else:
                GAME_SCENE = 6

        if BOT_STATE == "game" and GAME_SCENE == 8:
            BOT_STATE = "replay"
            GAME_SCENE = 0
            bot.button(chat_id, "Wanna play again?", bot.initial_buttons['ReplayOrMenu'])

        if BOT_STATE == "replay" and GAME_SCENE == 0:
            if message_type == 'button' and data == "menu":
                BOT_STATE = "menu"
                bot.button(chat_id, "Click on a button from the main menu \U0001f447", bot.initial_buttons['Menu'])
            elif message_type == 'button' and data == "replay":
                BOT_STATE = "game"
                GAME_SCENE = 1
                bot.button(chat_id, "Send any symbol or emoji you want or click on one of the buttons",
                           bot.initial_buttons['StartGame'])

        config.update_cache(chat_id, parsed_message, BOT_STATE, GAME_SCENE)

        return Response('ok', status=200)

    else:
        return Response('denied', status=403)


def main():
    pass


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
