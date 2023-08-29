import calendar
from datetime import date, datetime

from dateutil.relativedelta import relativedelta


class Period:
    def __init__(self, start, end) -> None:
        self.end = end
        self.start = start

    def overlapping_days(self, another):
        overlapping_end = another.end if another.end < self.end else self.end
        overlapping_start = another.start if another.start > self.start else self.start
        return (overlapping_end - overlapping_start).days + 1


class BudgetService:
    def __init__(self, budget_repo):
        self.budget_repo = budget_repo

    def query(self, start: date, end: date) -> float:
        budgets = self.budget_repo.get_all()
        period = Period(start, end)
        return sum(map(lambda b: b.overlapping_amount(period), budgets))


class Budget:
    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def overlapping_amount(self, period):
        return period.overlapping_days(self._create_period()) * self._daily_amount()

    def _create_period(self):
        return Period(self._first_day(), self._last_day())

    def _first_day(self):
        return datetime.strptime(self.year_month, '%Y%m').date()

    def _last_day(self):
        return datetime.strptime(self.year_month + str(self._days()), '%Y%m%d').date()

    def _daily_amount(self):
        return self.amount / self._days()

    def _days(self):
        return calendar.monthrange(int(self.year_month[:4]), int(self.year_month[4:]))[1]


class BudgetRepo:
    def get_all(self):
        pass
