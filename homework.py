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
    def add_record(self, rec):
        self.records.append(rec)          
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

class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
    def get_calories_remained(self):
        today_remained: float = self.limit - self.get_today_stats()
        if today_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, ' 
                    f'но с общей калорийностью не более {today_remained} кКал')
        else:
            return 'Хватит есть!'

class CashCalculator(Calculator):
    USD_RATE: float = 72.0
    EURO_RATE: float = 86.0
    RUB_RATE: float = 1.0
    def get_today_cash_remained(self, currency):
        exchange_rate = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)}
        if currency not in exchange_rate:
            raise ValueError
        today_remained: float = self.limit - self.get_today_stats()
        if today_remained == 0:
            return f'Денег нет, держись'
        cash_remained = round(today_remained / exchange_rate[currency][1], 2)
        if today_remained > 0:
            return ('На сегодня осталось '
                    f'{cash_remained} {exchange_rate[currency][0]}')
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(cash_remained)} {exchange_rate[currency][0]}')

