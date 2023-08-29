from datetime import date
from collections import defaultdict
import calendar

from dateutil.relativedelta import relativedelta


class BudgetService:
    def __init__(self, budget_repo):
        self.budget_repo = budget_repo

    def _get_year_month_query_days_map(self, start, end):
        year_month_query_days_map = {}

        # no cross month
        start_year_month = start.strftime('%Y%m')
        end_year_month = end.strftime('%Y%m')
        if start_year_month == end_year_month:
            year_month_query_days_map[start_year_month] = end.day - start.day + 1

        else:  # cross month

            current = start
            while current < end.replace(day=1) + relativedelta(months=1):
                current_year_month = current.strftime('%Y%m')
                if current_year_month == start_year_month:
                    year_month_query_days_map[start_year_month] = calendar.monthrange(start.year, start.month)[
                                                                      1] - start.day + 1
                elif current_year_month == end_year_month:
                    year_month_query_days_map[end_year_month] = end.day
                else:
                    year_month_query_days_map[current_year_month] = \
                        calendar.monthrange(current.year, current.month)[
                            1]
                current = current + relativedelta(months=1)

        return year_month_query_days_map

    def query(self, start: date, end: date) -> float:
        budgets = self.budget_repo.get_all()
        year_month_query_days_map = {}
        # no cross month
        start_year_month = start.strftime('%Y%m')
        end_year_month = end.strftime('%Y%m')
        if start_year_month == end_year_month:
            year_month_query_days_map[start_year_month] = end.day - start.day + 1

        else:  # cross month

            current = start
            while current < end.replace(day=1) + relativedelta(months=1):
                current_year_month = current.strftime('%Y%m')
                if current_year_month == start_year_month:
                    overlapping_days = calendar.monthrange(start.year, start.month)[1] - start.day + 1
                    year_month_query_days_map[start_year_month] = overlapping_days
                elif current_year_month == end_year_month:
                    overlapping_days = end.day
                    year_month_query_days_map[end_year_month] = overlapping_days
                else:
                    overlapping_days = calendar.monthrange(current.year, current.month)[1]
                    year_month_query_days_map[current_year_month] = overlapping_days
                current = current + relativedelta(months=1)

        amount = 0
        for year_month, overlapping_days in year_month_query_days_map.items():
            filter_budgets = list(filter(lambda b: b.year_month == year_month, budgets))
            if len(filter_budgets) == 0:
                continue
            amount += filter_budgets[0].daily_amount() * overlapping_days

        return amount


class Budget:
    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def daily_amount(self):
        number_of_day = calendar.monthrange(int(self.year_month[:4]), int(self.year_month[4:]))[1]
        return self.amount / number_of_day


class BudgetRepo:
    def get_all(self):
        pass
