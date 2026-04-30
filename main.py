"""
Задача: "Параллельный мониторинг криптовалют"

Тебе нужно написать систему, которая одновременно отслеживает цены нескольких монет 
с публичного API (CoinGecko — без ключа), обрабатывает их с ограничением на количество 
одновременных запросов, и пишет отчёт в файл.

ЧТО НУЖНО СДЕЛАТЬ

✓ Взять список из 20 монет (bitcoin, ethereum, solana, … и т.д.)
✓ Асинхронно запросить цену каждой монеты через CoinGecko API
✓ Ограничить одновременные запросы — не более 5 через asyncio.Semaphore
✓ Запустить всё через asyncio.gather() и собрать результаты
✓ Некоторые монеты намеренно "сломаны" (невалидный ID) — обработать ошибки не падая
✓ Записать итоговый отчёт в report.json с ценами, временем запроса и статусом
БОНУСНЫЕ ЗАДАНИЯ

Добавить retry логику: если запрос упал — повторить до 3 раз с экспоненциальной задержкой
Запускать мониторинг каждые 60 секунд в бесконечном цикле через asyncio.sleep()
Вывести live-progress в консоль: сколько запросов выполнено из 20
"""

"""
Plan:
1)Создать список из монет
2)Делать запрос с помощью CoinGecko
3)Запрашивать с помощью этого апи цену на монету
4)Создать скрипт asyncio который будет одновременно узнавать цену 5 монет
5)Выводить все это в консоль
6)Добавлять значения в dict, 
  {
  "coin": "bitcoin",
  "price": 76786.45,
  "currency": "usd",
  "status": "ok",
  "requested_at": "..."
}
7)Если монеты сломанны, то обробатывать ошибку, что бы код не падал, try, except
8)Потом добавить в мой скрипт что бы писалось время когда мы узнали цену крипты
9)Добавить строку статус, ли все удалось узнать, если да, писать статус ок, если нет, то статус ноу
10)Создать папку report.json, в который будут идти все мои данные с ценами, временем и статусом
11)Дальше идет ДОП, сначала сделать все что сверху

"""

# import asyncio
# import requests

# url = "https://api.coingecko.com/api/v3/simple/price"
# params = {
# "ids": "bitcoin,ethereum",
#     "vs_currencies": "usd"
# }

# headers = 

# resp = requests.get()

import requests
from datetime import datetime
import asyncio
import json



def write_report(crypto):
    with open(f'./lesson52/report.json','w')as file:
        json.dump(crypto,file,indent=4)

        
async def create_parse_response(coin):
    tries = 0
    delay = int(15)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin,
        "vs_currencies": "usd"
    }
    # await asyncio.sleep(1)
    # response.raise_for_status()
    while tries < 3:
        response = requests.get(url, params=params)
        if response.status_code == 429:
            await asyncio.sleep(delay)
            delay += 10
            tries += 1
        else:
            break
    if tries == 3:
        data = 'status'
        return data
    data = response.json()
    print(data)
    return data


async def create_dictionary(crypto,coin,price,status,time_parse):
    crypto.append({
        "coin": coin,
        "price": price,
        "currency": "usd",
        "status": status,
        "requested_at": time_parse
    })


async def func_sem(coin,semaphore,crypto):
    async with semaphore:
        data = await create_parse_response(coin)
        time_parse = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'status' in data:
            price = None
            status = 'rate limit'
            print('coin rate limit')
        elif coin in data:
            price = data[coin]['usd']
            print(f"{coin} price: {price} USD")
            status = 'ok'
        else:
            print(f'{coin} is not found')
            price = None
            status = "not found"
        await create_dictionary(crypto,coin,price,status,time_parse)


async def main():
    semaphore = asyncio.Semaphore(2)
    func_coins = ['bitcoin','ethereum','uniswap','solana','BNB','dogecoin','cardano','chainlink','aster','pepe','aave','ondo','worldcoin','arbitrum','cosmos','render','aptos','raydium','pendle','celestia']
    crypto = []
    tasks = []

    for coin in func_coins:
        tasks.append(asyncio.create_task(func_sem(coin,semaphore,crypto)))
    await asyncio.gather(*tasks)
    write_report(crypto)
    print(crypto)

asyncio.run(main())