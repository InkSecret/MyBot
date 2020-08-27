import telebot, pprint, requests
bot = telebot.TeleBot('1297743641:AAHLWQGAr9CK9U3fEhx5syFvpecZRt0WPnM')
sign = ('Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы')

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Привет ты написал мне')
    elif message.text == '/help':
        text = 'Доступные комманды:\n\nПривет\nПока\nЯ тебя люблю\nВалюта\nОтправить стикер'
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def send_message(message):
    text = message.text.lower()
    if text == 'привет':
        bot.send_message(message.chat.id, 'Привет мой создатель')
    elif text == 'пока':
        bot.send_message(message.chat.id, 'Прощай создатель')
    elif text == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANsX0bIrdLq9sy1kUPv7x78X-v7AdYAAmkAA6bKyAzjWDnq_QePXBsE')
    elif text == 'валюта':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(telebot.types.InlineKeyboardButton('USD', callback_data='get-vallet-usd'))        
        keyboard.row(
            telebot.types.InlineKeyboardButton('EUR', callback_data='get-vallet-eur'),
            telebot.types.InlineKeyboardButton('RUB', callback_data='get-vallet-rub')
            )    
        bot.send_message(message.chat.id, 'Посмотреть курс валют:', reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_location(message):
    api_key = '972c30fbde4e73d309d485f124b29331'
    data = {'lat':message.location.latitude, 'lon':message.location.longitude, 'APPID': api_key}
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}'.format(message.location.latitude, message.location.longitude, api_key)
    req = requests.post(url).json()
    output = 'City: %s\n' % (req['name'])
    bot.send_message(message.chat.id, output)
    print(req)

@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    bot.send_message(message.chat.id, 'Name => %s\nEmoji => %s\nStiker id => %s'%(message.sticker.set_name, message.sticker.emoji, message.sticker.file_id))

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data.startswith('get-vallet'):
        course = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11').json()
        index_cours = 0
        if call.data.endswith('usd'): index_cours = 0
        elif call.data.endswith('eur'): index_cours = 1
        elif call.data.endswith('rub'): index_cours = 2
        mess = '<b>UAH - %s</b>\n\nКупить: %s\nПродать: %s' % (course[index_cours]['ccy'], course[index_cours]['sale'], course[index_cours]['buy'])
        bot.send_message(call.message.chat.id, mess, parse_mode='html')

bot.polling()