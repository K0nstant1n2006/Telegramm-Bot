import telebot  # подключаем нужные библеотеки
from telebot import types
import random

bot = telebot.TeleBot('5106445021:AAGMrrBcrvafqddQokU82_JzsVjYVB3y-cw')  # токен бота
stones = 25  # количество камней
bot_answers = ['Пожалуй, я возьму', 'Наверно, мне стоит взять', 'Сочту нужным взять']  # реплики бота
TURN = 'player'  # переменная, позволяющая определять кто победит


def brat_kamni(id):  # функция, которая спрашивает у пользователя сколько камней он хочет взять
    but_1 = types.KeyboardButton('1')
    but_2 = types.KeyboardButton('2')
    but_3 = types.KeyboardButton('3')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # добавляется клавиатура
    markup.add(but_1)  # добавляются кнопочки
    markup.add(but_2)
    markup.add(but_3)
    bot.send_message(id, 'Сколько камней ты хочешь взять?', reply_markup=markup)  # бот отправляет сообщение


@bot.message_handler(commands=['start'])  # бот начинает работать по команде "/start"
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # добавляется клавиатура
    but_davai = types.KeyboardButton('Давай!')
    markup.add(but_davai)  # добавляется кнопочка
    bot.send_message(message.chat.id, 'Привет. Я Бот-Псевдоним. Давай сыграем в игру?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global stones  # делаем глобальными переменные stones и TURN
    global TURN
    if message.text == 'Давай!':
        bot.send_message(message.from_user.id, 'Игра заключается в следующем:')  # коротенький свод правил
        bot.send_message(message.from_user.id, '1)Есть кучка состоящая из 25 камней')
        bot.send_message(message.from_user.id, '2)Можно брать либо 1, либо 2, либо 3 камня')
        bot.send_message(message.from_user.id, '3)Кто возмет последний камень - победит.')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # добавляем клавиатуру
        but_da = types.KeyboardButton('Да!')
        markup.add(but_da)  # добавляется кнопочка
        bot.send_message(message.chat.id, 'Начнем?', reply_markup=markup)
    elif message.text == 'Да!':
        brat_kamni(message.chat.id)
    elif message.text == '1' or message.text == '2' or message.text == '3':
        kolvo = int(message.text)
        if kolvo > stones:  # на случай, если пользователь захотел взять больше камней, чем имеется
            bot.send_message(message.chat.id, 'Попробуй взять чуть меньше камней')
            brat_kamni(message.chat.id)
        else:
            stones -= kolvo
            bot.send_message(message.chat.id, f'Камней осталось {stones}')
            if stones == 0:
                bot.send_message(message.chat.id, f'Вы победили!')  # когда камни закончились, бот объявляет победителя
                bot.stop_polling()  # и завершает работу
            k_k = random.choice([1, 2, 3])  # бот "выбирает" сколько камней взять
            while k_k > stones:  # на случай, если бот захотел взять больше камней, чем имеется
                k_k = random.choice([1, 2, 3])
            if k_k == 1:
                bot.send_message(message.chat.id, f'{random.choice(bot_answers)} {k_k} камень')
            else:
                bot.send_message(message.chat.id, f'{random.choice(bot_answers)} {k_k} камня')
            TURN = 'bot'
            stones -= k_k
            bot.send_message(message.chat.id, f'Камней осталось {stones}')
            if stones == 0:
                bot.send_message(message.chat.id, f'Победил я!')  # когда камни заканчиваются, бот объявляет победителя
                bot.stop_polling()  # и завершает работу
            TURN = 'player'
            brat_kamni(message.chat.id)


bot.polling(none_stop=True, interval=0)
