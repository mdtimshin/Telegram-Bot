import telebot
from telebot import types
from pycbrf.toolbox import ExchangeRates
import datetime

bot = telebot.TeleBot('5913649800:AAFH62jzJCnbdwvXLyaPDk3F-M7U2oED6D8')
today = str(datetime.datetime.now().date())

board = {1: ' ', 2: ' ', 3: ' ',
         4: ' ', 5: ' ', 6: ' ',
         7: ' ', 8: ' ', 9: ' '}

player = 'X'
computer = 'O'


def printBoard():
    btn = types.InlineKeyboardButton
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        btn(board[1], callback_data='1'),
        btn(board[2], callback_data='2'),
        btn(board[3], callback_data='3'),
        btn(board[4], callback_data='4'),
        btn(board[5], callback_data='5'),
        btn(board[6], callback_data='6'),
        btn(board[7], callback_data='7'),
        btn(board[8], callback_data='8'),
        btn(board[9], callback_data='9'),
    )
    return {
        'text': 'Поле',
        'parse_mode': 'html',
        'reply_markup': markup
    }


def spaceIsFree(position):
    if board[position] == ' ':
        return True
    return False


def insertLetter(call, letter, position):
    if spaceIsFree(position):
        board[position] = letter
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, **printBoard())
        if checkDraw():
            bot.send_message(call.message.chat.id, text='Ничья!')
            keyboard = types.InlineKeyboardMarkup()
            key_rate = types.InlineKeyboardButton(text='Курсы валют', callback_data='get_rate')
            keyboard.add(key_rate)
            key_rate = types.InlineKeyboardButton(text='Игра "Крестики нолики"', callback_data='game_tic_tac_toe')
            keyboard.add(key_rate)
            bot.send_message(call.message.chat.id, text='Выбери действие, которое хочешь сделать',
                             reply_markup=keyboard)
        if checkWin():
            if letter == computer:
                bot.send_message(call.message.chat.id, text='Бот выиграл!')
            else:
                bot.send_message(call.message.chat.id, text='Ты выиграл!')
        return True
    else:
        bot.send_message(call.message.chat.id, text='Неверная позиция')
        return False


def checkWin():
    if (board[1] == board[2] and board[1] == board[3] and board[1] != ' '):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] != ' '):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] != ' '):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] != ' '):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] != ' '):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] != ' '):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] != ' '):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] != ' '):
        return True
    else:
        return False


def checkWhichMarkWon(mark):
    if (board[1] == board[2] and board[1] == board[3] and board[1] == mark):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] == mark):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] == mark):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] == mark):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] == mark):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] == mark):
        return True
    else:
        return False


def checkDraw():
    for key in board.keys():
        if board[key] == ' ':
            return False
    return True


def playerMove(call, position):
    position = int(position)
    insertLetter(call, player, position)
    return


def compMove(call):
    bestScore = -800
    bestMove = 0
    for key in board.keys():
        if board[key] == ' ':
            board[key] = computer
            score = minimax(False)
            board[key] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = key
    if bestMove in board:
        insertLetter(call, computer, bestMove)
    return


def minimax(isMaximizing):
    if checkWhichMarkWon(computer):
        return 1
    elif checkWhichMarkWon(player):
        return -1
    elif checkDraw():
        return 0

    if isMaximizing:
        bestScore = -800
        for key in board.keys():
            if board[key] == ' ':
                board[key] = computer
                score = minimax(False)
                board[key] = ' '
                if score > bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 800
        for key in board.keys():
            if board[key] == ' ':
                board[key] = player
                score = minimax(True)
                board[key] = ' '
                if score < bestScore:
                    bestScore = score
        return bestScore


@bot.callback_query_handler(func=lambda call: call.data.startswith(('X', 'O')))
def callback_worker_choose_player(call):
    global board
    global player
    global computer
    board = {1: ' ', 2: ' ', 3: ' ',
             4: ' ', 5: ' ', 6: ' ',
             7: ' ', 8: ' ', 9: ' '}
    if call.data == 'X':
        player = 'X'
        computer = 'O'
        bot.send_message(call.message.chat.id, **printBoard())
    else:
        player = 'O'
        computer = 'X'
        compMove(call)


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def callback_worker_game(call):
    if insertLetter(call, player, int(call.data)):
        compMove(call)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "get_rate":
        keyboard = types.InlineKeyboardMarkup()
        key_rate = types.InlineKeyboardButton(text='Доллар USD', callback_data='get_rate_USD')
        keyboard.add(key_rate)
        key_rate = types.InlineKeyboardButton(text='Евро EUR', callback_data='get_rate_EUR')
        keyboard.add(key_rate)
        key_rate = types.InlineKeyboardButton(text='Фунт стерлингов GBP', callback_data='get_rate_GBP')
        keyboard.add(key_rate)
        key_rate = types.InlineKeyboardButton(text='Швейцарский франк CHF', callback_data='get_rate_CHF')
        keyboard.add(key_rate)
        key_rate = types.InlineKeyboardButton(text='Японская иена JPY', callback_data='get_rate_JPY')
        keyboard.add(key_rate)
        bot.send_message(call.message.chat.id, 'Выбери курс интересующей тебя валюты', reply_markup=keyboard)
    elif call.data == "get_rate_USD":
        rates = ExchangeRates(today)
        rate = rates['USD'].rate
        bot.send_message(call.message.chat.id, f'Курс доллара = {rate} руб.')
    elif call.data == "get_rate_EUR":
        rates = ExchangeRates(today)
        rate = rates['EUR'].rate
        bot.send_message(call.message.chat.id, f'Курс евро = {rate} руб.')
    elif call.data == "get_rate_GBP":
        rates = ExchangeRates(today)
        rate = rates['GBP'].rate
        bot.send_message(call.message.chat.id, f'Курс фунта стерлингов = {rate} руб.')
    elif call.data == "get_rate_CHF":
        rates = ExchangeRates(today)
        rate = rates['CHF'].rate
        bot.send_message(call.message.chat.id, f'Курс франка = {rate} руб.')
    elif call.data == "get_rate_JPY":
        rates = ExchangeRates(today)
        rate = rates['JPY'].rate
        bot.send_message(call.message.chat.id, f'Курс иены = {rate} руб.')
    elif call.data == "game_tic_tac_toe":
        # gmap = u'''
        #         ██████████
        #         ██████ . █
        #         █  ◯☿◯ ◯ █
        #         █     ..██
        #         ██████████
        #     '''.replace('\n        ', '\n')
        bot.send_message(call.message.chat.id, 'Это игра "Крестики-нолики"')
        global board
        board = {1: ' ', 2: ' ', 3: ' ',
                 4: ' ', 5: ' ', 6: ' ',
                 7: ' ', 8: ' ', 9: ' '}
        keyboard = types.InlineKeyboardMarkup()
        moveX = types.InlineKeyboardButton(text='X', callback_data='X')
        moveO = types.InlineKeyboardButton(text='O', callback_data='O')
        keyboard.add(moveX, moveO)
        bot.send_message(call.message.chat.id, text='Выбери сторону', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Привет' or '/start':
        bot.send_message(message.from_user.id, "Привет, я mdtimshin бот")
        keyboard = types.InlineKeyboardMarkup()
        key_rate = types.InlineKeyboardButton(text='Курсы валют', callback_data='get_rate')
        keyboard.add(key_rate)
        key_rate = types.InlineKeyboardButton(text='Игра "Крестики нолики"', callback_data='game_tic_tac_toe')
        keyboard.add(key_rate)
        bot.send_message(message.from_user.id, text='Выбери действие, которое хочешь сделать', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
