from background import keep_alive
from telebot import types
from telebot import custom_filters
import time
import requests
from bs4 import BeautifulSoup
import json
from web3 import Web3
import telebot
import configure
import sqlite3
import datetime

bot = telebot.TeleBot(configure.config["token"], threaded=True, num_threads=300)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.ChatFilter())


@bot.message_handler(commands=["start"])
def start(message, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Узнать обстановку")
    markup.add(button1)

    # Добавление юзера в бд при старте
    def register_new_user(user_id, nickname, username):
        register_user = "INSERT OR IGNORE INTO test (user_id, nickname, username) VALUES (?, ?, ?)"
        columns = (user_id, nickname, username)
        cursor.execute(register_user, columns)
        conn.commit()

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    username = message.from_user.username

    register_new_user(user_id=us_id, nickname=us_name, username=username)

    bot.reply_to(message, text="""*👋 Привет! Это бот для отслеживания обстановки Namars*
➖➖➖➖➖➖➖➖➖➖➖➖➖
⏰ Информация обновляется каждый раз когда вы нажимаете кнопку
➖➖➖➖➖➖➖➖➖➖➖➖➖
💜 Для пользования ботом нужно быть подписанным на @halavayahunt
➖➖➖➖➖➖➖➖➖➖➖➖➖
❗ Иногда могут быть ошибки в работе бота , не серчайте
➖➖➖➖➖➖➖➖➖➖➖➖➖
❗ Если возникли вопросы или проблемы, пропишите /help
➖➖➖➖➖➖➖➖➖➖➖➖➖
💎 Поддержать автора - `0xF757f3A0E4593daF5fe5777b2C6bA1D8a1ec6d44`
➖➖➖➖➖➖➖➖➖➖➖➖➖
*💜 Спасибо! *
""", parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(text=['Узнать обстановку'])
def get_info(message):
    date = datetime.datetime.today()
    print("Получил запрос на обстановку от", message.from_user.first_name, ", время запроса =",
          date.strftime('%H:%M:%S %m.%d '))
    # Проверка того что юзер состоит в группе
    chat_id = -1001790926622
    user_id = message.from_user.id
    user_channel_status = bot.get_chat_member(chat_id, user_id)
    if user_channel_status.status == 'left':
        bot.send_message(message.chat.id, '* Подпишитесь @halavayahunt чтобы пользоваться ботом💜 *',
                         parse_mode="Markdown")
    else:
        # Спот
        response = requests.get("https://yobit.net/api/3/ticker/wrub_rur")
        soup = BeautifulSoup(response.text, "lxml")
        price_tag = soup.find("body")
        for data in price_tag:
            price_json = json.loads(data.string)

        response_spot = f"1 врабчик на споте = {str(price_json['wrub_rur']['last'])[0:5]} RUB"

        # DEFI
        response2 = requests.get("https://yobit.net/api/defi/info/wrub_rur")
        soup2 = BeautifulSoup(response2.text, "lxml")
        price_tag2 = soup2.find("body")
        for data in price_tag2:
            price_json2 = json.loads(data.string)

        response_defi = f"1 врабчик в DEFI = {price_json2['pools']['wrub_rur']['price1'][0:5]} RUB"

        # проверка баланса бнб
        wallet_address_namars = '0x0064838E894271F0f568DBa3b202C7A7F9723599'
        balance_namars = web3.eth.get_balance(wallet_address_namars)
        response_bnb_namars = f"Баланс BNB Namars = {round(balance_namars / 10 ** 18, 3)} BNB"

        wallet_address_yobit = '0x097A40BF3bdA3058a8683990A15CEf5C2f1fd3D4'
        balance_yobit = web3.eth.get_balance(wallet_address_yobit)
        response_bnb_yobit = f"Баланс BNB Yobit = {round(balance_yobit / 10 ** 18, 3)} BNB"

        # проверка баланса врабчика
        # Вводим аби токена
        WRUB_ABI = json.loads(
            '''[{"inputs":[{"internalType":"string","name":"name_","type":"string"},{"internalType":"string","name":"symbol_","type":"string"},{"internalType":"uint256","name":"decimals_","type":"uint256"},{"internalType":"uint256","name":"initialBalance_","type":"uint256"},{"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"address payable","name":"feeReceiver_","type":"address"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"Optimization","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"tokenAmount","type":"uint256"}],"name":"recoverERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]''')

        # WRUB токен
        wrub_contract_address = '0x72f74Fb5382a7A49B5c6e8437A04D65bf2ff5736'

        # инициализация контракта
        wrub_contract = web3.eth.contract(wrub_contract_address, abi=WRUB_ABI)

        balance_of_token = wrub_contract.functions.balanceOf(wallet_address_namars).call()  # in Wei
        wrub_balance = balance_of_token / 10 ** 18

        def format_number(number):
            number = str(number)[::-1]
            result = ''
            for i, num in enumerate(number):
                if i % 3 == 0:
                    result += '.'
                result += num
            result = result[::-1][:-1]
            return result

        wrub_balance_formatted = format_number(int(wrub_balance))

        cursor.execute("SELECT status_text FROM test WHERE user_id = ?", (702999620,))
        response_withdrawals = cursor.fetchone()
        response_withdrawals = response_withdrawals[0]
        response_wrub_count = f"Баланс врабчиков = {wrub_balance_formatted} WRUB"

        bot.send_message(message.chat.id, f""" 🔥 * Обстановка Namars * 🔥
➖➖➖➖➖➖➖➖➖➖➖
💰 {response_wrub_count}
➖➖➖➖➖➖➖➖➖➖➖
🏆 {response_bnb_namars}
➖➖➖➖➖➖➖➖➖➖➖
🏆 {response_bnb_yobit}
➖➖➖➖➖➖➖➖➖➖➖
📈 {response_spot}
➖➖➖➖➖➖➖➖➖➖➖
📈 {response_defi} 
➖➖➖➖➖➖➖➖➖➖➖
💵 Статус выводов - {response_withdrawals}
""", parse_mode="Markdown")


@bot.message_handler(commands=["help"])
def request_group(message):
    bot.send_message(message.chat.id, text="""*👋 Привет! Это бот для отслеживания обстановки Namars*
➖➖➖➖➖➖➖➖➖➖➖➖➖
⏰ Информация обновляется каждый раз когда вы нажимаете кнопку
➖➖➖➖➖➖➖➖➖➖➖➖➖
💜 Бот создан таким же абузером намарса на чистом энтузиазме, так что не серчайте если будут какие то проблемы с ботом
➖➖➖➖➖➖➖➖➖➖➖➖➖
💜 Для пользования ботом нужно быть подписанным на @halavayahunt
➖➖➖➖➖➖➖➖➖➖➖➖➖
❗ Если бот не работает, попробуйте перезапустить его прописав /start
➖➖➖➖➖➖➖➖➖➖➖➖➖
✅ Если остались какие-либо вопросы или пожелания, не стесняйтесь писать в чат @huntschat либо в лс @ladno9867
➖➖➖➖➖➖➖➖➖➖➖➖➖
💎 Поддержать автора можете отправив любую монету в любой EVM сети на этот адрес - 
`0xF757f3A0E4593daF5fe5777b2C6bA1D8a1ec6d44`
➖➖➖➖➖➖➖➖➖➖➖➖➖
*💜 Спасибо! *
""", parse_mode="Markdown", )

@bot.message_handler(chat_id=[702999620], commands=['cmd'])
def show_admin_commands(message):
    bot.send_message(message.chat.id,
                     "✅ Изменить статус - /set_status\n\n"
                     "⏰ Изменить текст рассылки - /set_message\n\n"
                     "💎 Посчитать пользователей - /count_users\n\n"
                     "❗ Начать рассылку - /send_notification")

# Установка текста для рассылки
@bot.message_handler(chat_id=[702999620], commands=['set_message'])
def admin_update_notification(message):
    def update_notification_text(message_text: str):
        us_id = message.from_user.id
        sqlite_update_query = 'UPDATE test SET message_text = ? WHERE user_id = ?'
        column_values = (message_text, us_id)
        cursor.execute(sqlite_update_query, column_values)
        conn.commit()

    def update_text(message):
        new_text = message.text

        def input_text(message):
            msg = bot.reply_to(message)
            bot.register_next_step_handler(msg)
            new_text = message.text

        update_notification_text(message_text=new_text)
        cursor.execute("SELECT message_text FROM test WHERE user_id = ?", (702999620,))
        notification_text = cursor.fetchone()
        notification_text = notification_text[0]
        bot.send_message(message.chat.id, text=f"✅ Установлен текст для уведомления:\n{notification_text}",
                         parse_mode="Markdown")

    get_text = bot.reply_to(message, "❗ Введите новый текст для уведомления: ")
    bot.register_next_step_handler(get_text, update_text)

# Запуск рассылки
@bot.message_handler(chat_id=[702999620], commands=['send_notification'])
def admin_send_notification(message):
    bot.send_message(message.chat.id, "Вам разрешено использовать эту команду.")
    cursor.execute("SELECT user_id, message_text FROM test")
    matches = cursor.fetchall()
    d = dict(matches)

    amount_message = 0
    amount_bad = 0
    start_time = time.time()

    for user_id, message_text in d.items():
        try:
            cursor.execute("SELECT message_text FROM test WHERE user_id = ?", (702999620,))
            notification_text = cursor.fetchone()
            notification_text = notification_text[0]
            bot.send_message(user_id, text=notification_text, parse_mode="Markdown")
            amount_message += 1
        except:
            amount_bad += 1
            pass

    sending_time = time.time() - start_time
    bot.send_message(702999620,
                     f'✅Рассылка окончена\n'
                     f'❗Отправлено: {amount_message}\n'
                     f'❗Не отправлено: {amount_bad}\n'
                     f'🕐Время выполнения рассылки - {sending_time} секунд'
                     )

# Установка статуса выводов
@bot.message_handler(chat_id=[702999620], commands=['set_status'])
def admin_update_status(message):
    def update_status_text(status_text: str):
        us_id = message.from_user.id
        sqlite_update_query = 'UPDATE test SET status_text = ? WHERE user_id = ?'
        column_values = (status_text, us_id)
        cursor.execute(sqlite_update_query, column_values)
        conn.commit()

    def update_status(message):
        new_status_text = message.text

        def input_status(message):
            msg = bot.reply_to(message)
            bot.register_next_step_handler(msg)
            new_status_text = message.text

        bot.reply_to(message, f"✅ Установлен статус: {new_status_text}")
        update_status_text(status_text=new_status_text)

    get_status = bot.reply_to(message, "❗ Введите новый статус: ")
    bot.register_next_step_handler(get_status, update_status)

# Подсчет количества людей в боте
@bot.message_handler(chat_id=[702999620], commands=['count_users'])
def admin_count_users(message):
    bot.send_message(message.chat.id, "Вам разрешено использовать эту команду.")
    cursor.execute("SELECT user_id FROM test")
    matches = cursor.fetchall()
    users = list(matches)
    count_users = 0

    for user in users:
        if user:
            count_users += 1

    bot.send_message(702999620, f'✅ Количество пользователей в боте: {count_users}')

@bot.message_handler(commands=['set_message', 'set_status', 'count_users', 'send_notification', 'cmd'])
def not_admin(message):
    bot.send_message(message.chat.id, "Вам не разрешено использовать эту команду.")


if __name__ == "__main__":
    while True:
        try:
            # Подключение к бд
            conn = sqlite3.connect('db_main.db', check_same_thread=False)
            cursor = conn.cursor()

            # Подключение к RPC
            bsc_rpc = 'https://bsc.publicnode.com'
            web3 = Web3(Web3.HTTPProvider(endpoint_uri=bsc_rpc))
            print(f"Web3 is connected: {web3.is_connected()}")
            # Запуск бота
            keep_alive()
            bot.polling(skip_pending=True, none_stop=True)

        except Exception as e:
            telebot.logger.error(e)
            time.sleep(5)
