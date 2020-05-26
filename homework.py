import datetime as dt
from datetime import timedelta, datetime, date


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = (dt.datetime.now()).date()
        self.week_ago = (datetime.now() - timedelta(7)).date()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = 0
        for record in self.records:
            if record.date == self.today:
                day_stats += record.amount
        return day_stats

    def get_week_stats(self):
        week_stats = 0
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        for record in self.records:
            if record.date == self.today:
                self.limit -= record.amount
        if self.limit > 0:
            message = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.limit} кКал'
        else:
            message = f'Хватит есть!'
        return message


class CashCalculator(Calculator):
    USD_RATE = 70.0
    EURO_RATE = 77.0

    def __init__(self, limit):
        super().__init__(limit)
        self.records = []
        self.today = (dt.datetime.now()).date()
        self.week_ago = (datetime.now() - timedelta(7)).date()

    def get_today_cash_remained(self, currency):
        for record in self.records:
            if record.date == self.today:
                self.limit -= record.amount
        if currency == "usd":
            self.limit /= self.USD_RATE
            money = 'USD'
        elif currency == "eur":
            self.limit /= self.EURO_RATE
            money = 'Euro'
        else:
            money = 'руб'
        if self.limit > 0:
            message = f'На сегодня осталось {round(self.limit, 2)} {money}'
        elif self.limit == 0:
            message = f'Денег нет, держись'
        else:
            message = f'Денег нет, держись: твой долг - {abs(round(self.limit, 2))} {money}'
        return message


class Record:

    def __init__(self, amount, comment, date=(dt.datetime.now()).date()):
        self.amount = amount
        self.comment = comment
        if date == (dt.datetime.now()).date():
            self.date = date
        else:
            self.date = (dt.datetime.strptime(date, '%d.%m.%Y')).date()
