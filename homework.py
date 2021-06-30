import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator():

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        total = 0
        now = dt.date.today()
        for record in self.records:
            moment = record.date
            if now == moment:
                total += record.amount
        return total

    def get_week_stats(self):
        total = 0
        now = dt.date.today()
        week = (dt.date.today() - dt.timedelta(days=7))
        for record in self.records:
            moment = record.date
            if now >= moment >= week:
                total += record.amount
        return total

    def remain(self):
        today_remained: float = self.limit - self.get_today_stats()
        return today_remained


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.remain() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {self.remain()} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 72.03
    EURO_RATE = 86.21
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        remain = self.remain()
        exchange_rate = {
            'rub': (round(remain, 2), 'руб'),
            'usd': (round(remain / self.USD_RATE, 2), 'USD'),
            'eur': (round(remain / self.EURO_RATE, 2), 'Euro')}
        if currency not in exchange_rate:
            raise ValueError
        remain, currency = exchange_rate[currency]
        if remain == 0:
            return 'Денег нет, держись'
        if remain > 0:
            return f'На сегодня осталось {remain} {currency}'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(remain)} {currency}')
