import datetime as dt
from datetime import timedelta, datetime


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week_ago = (datetime.now() - timedelta(7)).date()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = []
        for record in self.records:
            if record.date == self.today:
                day_stats.append(record.amount)
        return sum(day_stats)

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)

    def get_today_limit_balance(self):
        limit_balance = self.limit - self.get_today_stats()
        return limit_balance


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = super().get_today_limit_balance()
        if calories_remained > 0:
            message = f'Сегодня можно съесть что-нибудь ещё, но с общей ' \
                      f'калорийностью не более {calories_remained} кКал'
        else:
            message = 'Хватит есть!'
        return message


class CashCalculator(Calculator):
    USD_RATE = 70.0
    EURO_RATE = 77.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub'):
        money_dic = {'usd': {'name': 'USD', 'rate': CashCalculator.USD_RATE},
                     'eur': {'name': 'Euro', 'rate': CashCalculator.EURO_RATE},
                     'rub': {'name': 'руб', 'rate': CashCalculator.RUB_RATE}}
        cash_remained = super().get_today_limit_balance()
        if cash_remained == 0:
            message = 'Денег нет, держись'
        elif currency not in money_dic:
            message = f'Валюта {currency} не поддерживается'
        elif cash_remained > 0:
            cash_remained = round(cash_remained /
                                  money_dic[currency]['rate'], 2)
            money = money_dic[currency]['name']
            message = f'На сегодня осталось {cash_remained} {money}'
        else:
            cash_remained = abs(round(cash_remained /
                                      money_dic[currency]['rate'], 2))
            money = money_dic[currency]['name']
            message = f'Денег нет, держись: твой долг - ' \
                      f'{cash_remained} {money}'
        return message


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date == None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
