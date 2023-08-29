from datetime import date
from collections import defaultdict
import calendar


class BudgetService:
    def __init__(self, budget_repo):
        self.budget_repo = budget_repo

    def _get_year_month_daily_budget_map(self):
        budgets = self.budget_repo.get_all()

        year_month_daily_budget_map = defaultdict(lambda: 0)

        for budget in budgets:
            year_month_daily_budget_map[budget.year_month] = budget.daily_amount()

        return year_month_daily_budget_map

    def _get_year_month_query_days_map(self, start, end):
        """
        Return:
            {
                '197001': 2,
                '197002': 1
            }
        """
        year_month_query_days_map = {}

        y_months = range(start.year * 12 + start.month, end.year * 12 + end.month)

        # no cross month
        if len(y_months) == 0:
            year_month_query_days_map[f'{start.year}{start.month:02d}'] = end.day - start.day + 1

        else:  # cross month
            # calculate first month
            year_month_query_days_map[f'{start.year}{start.month:02d}'] = calendar.monthrange(start.year, start.month)[
                                                                              1] - start.day + 1

            # calculate inner month
            if len(y_months) >= 2:
                for ym in y_months[1:]:
                    year = int(ym / 12)
                    month = ym % 12
                    year_month_query_days_map[f'{year}{month:02d}'] = calendar.monthrange(year, month)[1]

            # calculate last month
            year_month_query_days_map[f'{end.year}{end.month:02d}'] = end.day

        return year_month_query_days_map

    def query(self, start: date, end: date) -> float:
        budgets = self.budget_repo.get_all()
        # budget_map = defaultdict(lambda: 0)
        # for budget in budgets:
        #     budget_map[budget.year_month] = budget.daily_amount()
        # year_month_daily_budget_map = budget_map
        year_month_query_days_map = self._get_year_month_query_days_map(start, end)

        amount = 0
        for year_month, days in year_month_query_days_map.items():
            filter_budgets = list(filter(lambda b: b.year_month == year_month, budgets))
            if len(filter_budgets) == 0:
                continue
            amount += filter_budgets[0].daily_amount() * days
            # amount += year_month_daily_budget_map[year_month] * days

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
