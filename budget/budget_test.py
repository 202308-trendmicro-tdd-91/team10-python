import unittest
from datetime import date
from budget import BudgetService ,Budget

class MockedBudgetRepo:
    def get_all():
        pass

class BudgetTests(unittest.TestCase):

    def test_without_budget(self):
        mocked_budget_repo = MockedBudgetRepo()
        mocked_budget_repo.get_all = lambda: []
        budget_service = BudgetService(mocked_budget_repo)

        useless_start = date(1970, 1, 1)
        useless_end = date(1970, 1, 1)
        self.assertEqual(budget_service.query(useless_start, useless_end), 0)

    def test_single_day(self):
        mocked_budget_repo = MockedBudgetRepo()
        mocked_budget_repo.get_all = lambda: [Budget('197001', 3100)]
        budget_service = BudgetService(mocked_budget_repo)

        start = date(1970, 1, 1)
        end = date(1970, 1, 1)
        self.assertEqual(budget_service.query(start, end), 100)

    def test_cross_month(self):

        mocked_budget_repo = MockedBudgetRepo()
        mocked_budget_repo.get_all = lambda: [Budget('197001', 3100), Budget('197002', 4200)]
        budget_service = BudgetService(mocked_budget_repo)

        start = date(1970, 1, 30)
        end = date(1970, 2, 1)

        expected_amount = 2 * 100 + 1 * 150
        self.assertEqual(budget_service.query(start, end), expected_amount)

    def test_cross_three_month(self):

        mocked_budget_repo = MockedBudgetRepo()
        mocked_budget_repo.get_all = lambda: [Budget('197001', 3100), Budget('197002', 4200), Budget('197003', 620)]
        budget_service = BudgetService(mocked_budget_repo)

        start = date(1970, 1, 30)
        end = date(1970, 3, 15)

        expected_amount = 200 + 4200 + 300
        
        self.assertEqual(budget_service.query(start, end), expected_amount)