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
        # no cross month
        if start.strftime('%Y%m') == end.strftime('%Y%m'):
            filter_budgets = list(filter(lambda b: b.year_month == start.strftime('%Y%m'), budgets))
            if len(filter_budgets) == 0:
                return 0
            return (end.day - start.day + 1) * filter_budgets[0].daily_amount()

        else:  # cross month

            current = start
            total_amount = 0
            while current < end.replace(day=1) + relativedelta(months=1):
                current_year_month = current.strftime('%Y%m')
                filter_budgets = list(filter(lambda b: b.year_month == current_year_month, budgets))
                if len(filter_budgets) == 0:
                    continue

                budget = filter_budgets[0]
                period = Period(start, end)
                another = Period(budget.first_day(), budget.last_day())
                total_amount += period.overlapping_days(another) * budget.daily_amount()
                current = current + relativedelta(months=1)

            return total_amount


class Budget:
    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def first_day(self):
        return datetime.strptime(self.year_month, '%Y%m').date()

    def last_day(self):
        return datetime.strptime(self.year_month + str(self.days()), '%Y%m%d').date()

    def daily_amount(self):
        return self.amount / self.days()

    def days(self):
        return calendar.monthrange(int(self.year_month[:4]), int(self.year_month[4:]))[1]


class BudgetRepo:
    def get_all(self):
        pass
