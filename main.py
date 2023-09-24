import asyncio
import time
import requests
from bs4 import BeautifulSoup
import json
from web3 import Web3
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types, asyncio_filters
import configure

bot = AsyncTeleBot(configure.config["token"])
bot.add_custom_filter(telebot.asyncio_filters.TextMatchFilter())


def task(number):
    number = str(number)[::-1]
    result = ''
    for i, num in enumerate(number):
        if i % 3 == 0:
            result += '.'
        result += num
    result = result[::-1][:-1]
    return result


@bot.message_handler(commands=["start"])
async def start(message, res=False ):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Узнать обстановку")
    markup.add(button1)
    await bot.reply_to(message, text="""*✅ Это бот для отслеживания обстановки Namars.*
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
⏰ Информация обновляется каждый раз когда вы нажимаете кнопку.
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💎 Поддержать автора - `0xF757f3A0E4593daF5fe5777b2C6bA1D8a1ec6d44`
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
❗ Иногда может показывать статус выводов неправильно, не серчайте.
""", parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(text=['Узнать обстановку'])
async def enable(message, last_tx=0):
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

    # Чекаем адреса
    bsc_rpc = 'https://bsc.publicnode.com'
    web3 = Web3(Web3.HTTPProvider(endpoint_uri=bsc_rpc))

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
    token_decimals = wrub_contract.functions.decimals().call()

    wrub_balance = balance_of_token / 10 ** token_decimals
    wrub_balance_formatted = task(int(wrub_balance))

    response_wrub_count = f"Баланс врабчиков = {wrub_balance_formatted} WRUB"

    await bot.send_message(message.chat.id, f""" 🔥 * Обстановка Namars * 🔥
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

@bot.message_handler(text=['Help'])
async def request_group(message):
    await bot.send_message(message.chat.id, text="""*✅ Это бот для отслеживания обстановки Namars.*
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
⏰ Информация обновляется каждый раз когда вы нажимаете кнопку.
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💎 Поддержать автора - `0xF757f3A0E4593daF5fe5777b2C6bA1D8a1ec6d44`
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
❗ Иногда может показывать статус выводов "выводит" неправильно, не серчайте.
""", parse_mode="Markdown")


if __name__ == "__main__":
    while True:
        try:
            last_tx = 0
            response_withdrawals = ''
            bsc_rpc = 'https://bsc.publicnode.com'
            web3 = Web3(Web3.HTTPProvider(endpoint_uri=bsc_rpc))

            # Проверка количества транз
            wallet_address_namars = '0x0064838E894271F0f568DBa3b202C7A7F9723599'
            tx_count = web3.eth.get_transaction_count(wallet_address_namars)

            if last_tx > tx_count:
                response_withdrawals = 'выводит!!!'
                last_tx = tx_count
            else:
                response_withdrawals = 'не выводит, скам'

            asyncio.run(bot.polling(skip_pending=True))
        except Exception as e:
            telebot.logger.error(e)
            time.sleep(15)
