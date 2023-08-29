import calendar
from datetime import date, datetime

from dateutil.relativedelta import relativedelta


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
                overlapping_days = self.overlapping_days(budget, end, start)
                total_amount += overlapping_days * budget.daily_amount()
                current = current + relativedelta(months=1)

            return total_amount

    def overlapping_days(self, budget, end, start):
        if budget.year_month == start.strftime('%Y%m'):
            overlapping_end = budget.last_day()
            overlapping_start = start
        elif budget.year_month == end.strftime('%Y%m'):
            overlapping_end = end
            overlapping_start = budget.first_day()
        else:
            overlapping_end = budget.last_day()
            overlapping_start = budget.first_day()
        overlapping_days = (overlapping_end - overlapping_start).days + 1
        return overlapping_days


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
