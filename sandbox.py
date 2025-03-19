from binance import AsyncClient, BinanceSocketManager
from telebot.async_telebot import AsyncTeleBot
class Exchange:
    def __init__(self, exchange, fee, stop):
        self.fee = fee
        self.stop = stop/100
        self.exchange = exchange
        self.balance = {}
        self.balance_usdt = 100
        self.balance_usdt_old = 0
        self.price_list = {}
        self.channel = ""
        self.telegram_bot_token = ''
        self.bot = AsyncTeleBot(self.telegram_bot_token)
        self.streams = ["btctusd@bookTicker"]
        self.stop_list = {}

    async def buy(self, pair):
        price = self.price_list[pair]['ask']
        if self.balance_usdt != 0:
            if pair in self.balance:
                if self.balance[pair]['status'] == 0:
                    amount = self.balance_usdt/price - self.balance_usdt/price * self.fee
                    self.balance[pair]['bal'] = amount
                    self.balance_usdt_old = self.balance_usdt
                    self.balance_usdt = 0
                    self.balance[pair]['status'] = 1
                    await self.create_stop(pair=pair)
                    print(f"Buy {pair} {self.exchange} {price} amount: {amount}")
            else:
                self.balance[pair] = {'status':0, 'bal':0}
                await self.buy(pair=pair)
    # usdt -> btc = usdt_q/btc_price - usdt_q/btc_price * fee 

    async def sell(self, pair, typ):
        price = self.price_list[pair]['bid']
        if pair in self.balance:
            if 'bal' in self.balance[pair]:
                if self.balance[pair]['bal'] != 0:
                    if self.balance[pair]['status'] == 1:
                        amount = self.balance[pair]['bal']*price - self.balance[pair]['bal']*price * self.fee
                        self.balance_usdt = amount
                        profit = amount - self.balance_usdt_old
                        self.balance_usdt_old = amount
                        self.balance[pair]['bal'] = 0
                        self.balance[pair]['status'] = 0
                        print(f"Sell {pair} {self.exchange} {price} amount: {amount} profit: {profit}")
                        await self.sendmsg(msg=f"• Пара: {pair}💎 \n• Цена: {price}📉 \n• Профит: {profit}<strong>$</strong>\n• Баланс: {amount}<strong>$</strong>\n• Тип: {typ}💎")
                        
        else: 
            self.balance[pair] = {'status':0, 'bal':0}
    async def sendmsg(self, msg):
        await self.bot.send_message(self.channel, msg, parse_mode="html")

    async def prices(self):
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)            
        ms = bm.multiplex_socket(self.streams)
        async with ms as tscm:
            while True:
                res = await tscm.recv()
                await self.on_message(msg=res)
    async def on_message(self, msg):
        # print(msg)
        dt = {}
        dt['ask'] = float(msg['data']["a"])
        dt['bid'] = float(msg['data']["b"])
        d = { str(msg["data"]["s"]).lower(): dt}
        self.price_list.update(d)
        # print(self.price_list)
        await self.stop_update()

    async def create_stop(self, pair):
        price = self.price_list[pair]['bid'] - self.price_list[pair]['bid']*self.stop
        if pair not in self.stop_list:
            self.stop_list[pair] = {'price':price, "pair":pair, "status":True}
        if pair in self.stop_list:
            if self.stop_list[pair]['status'] == False:
                self.stop_list[pair]['status'] = True

    async def stop_update(self):
        for i in self.stop_list:
            # print(i)
            if self.stop_list[i]['status'] == True:
                if self.price_list[i]['bid'] <= self.stop_list[i]['price']:
                    await self.sell(pair=i, typ="stoploss")
                    self.stop_list[i]['status'] = False


    # async def run(self):
    #     task1 = asyncio.create_task(self.prices())
    #     task2 = asyncio.create_task(self.stop_update())
    #     await asyncio.gather(task1, task2)


    # usdt -> btc = btc_q/btc_price - btc_q/btc_price * fee 
# async def main(bina):
#     await asyncio.sleep(3)
#     await bina.buy("btctusd")
#     # pass
# async def run():
#     bina = Exchange("binance", 0.0, 0.01)
#     # task=asyncio.create_task(bina.run())
#     price = asyncio.create_task(bina.prices())
#     # stop = asyncio.create_task(bina.stop_update())
#     task2=asyncio.create_task(main(bina))
#     await asyncio.gather(task2, price)
# asyncio.run(run())