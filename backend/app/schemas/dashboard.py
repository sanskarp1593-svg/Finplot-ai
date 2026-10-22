"""Pydantic schemas for the dashboard endpoint."""

from __future__ import annotations

from pydantic import BaseModel


class MonthSummary(BaseModel):
    month: str          # "YYYY-MM"
    revenue: float
    expenses: float
    profit: float
    margin: float       # profit / revenue  (0 if no revenue)


class MonthChange(BaseModel):
    revenue_change: float | None = None   # % change vs previous month
    expenses_change: float | None = None
    profit_change: float | None = None


class SparklinePoint(BaseModel):
    month: str
    value: float


class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float   # of total expenses


class BudgetProgress(BaseModel):
    category: str
    spent: float
    limit: float
    percentage: float   # spent / limit * 100
    over_budget: bool


class DashboardData(BaseModel):
    summary: MonthSummary
    change: MonthChange
    sparkline_revenue: list[SparklinePoint]
    sparkline_expenses: list[SparklinePoint]
    sparkline_profit: list[SparklinePoint]
    trend: list[MonthSummary]
    category_breakdown: list[CategoryBreakdown]
    budget_progress: list[BudgetProgress]
    gemini_available: bool = False
