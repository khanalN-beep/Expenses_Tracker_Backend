from django.db.models import Sum
from expenses.models import Expense


def calculate_monthly_summary(user, budget):
    # The total spent
    total_spent = (
        Expense.objects.filter(user=user, budget=budget)
        .aggregate(total=Sum("amount"))
        .get("total", 0)
    )

    # remaining balance
    balance = budget.monthly_budget - total_spent
    percentage = (
        (total_spent / budget.monthly_budget) * 100
        if budget.monthly_budget > 0
        else 0
    )

    # category breakdown
    category_data = (
        Expense.objects.filter(user=user, budget=budget)
        .values("category_name")
        .annotate(total=Sum("amount"))
    )

    category_breakdown = {
        item["category_name"] or "Unknown": item["total"]
        for item in category_data
    }

    # daily expenses
    daily_expenses = list(
        Expense.objects.filter(user=user, budget=budget)
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )

    # biggest expense
    biggest = (
        Expense.objects.filter(user=user, budget=budget)
        .order_by("-amount")
        .first()
    )

    biggest_expense = (
        {
            "title": biggest.title,
            "amount": biggest.amount,
            "category": biggest.category_name.name if biggest.category_name else "Unknown",
            "date": biggest.date,
        }
        if biggest
        else {}
    )

    return {
        "month": budget.month,
        "year": budget.year,
        "monthly_budget": budget.monthly_budget,
        "total_spent": total_spent,
        "balance": balance,
        "profit_or_loss": "Profit" if balance >= 0 else "Loss",
        "percentage": percentage,
        "category_breakdown": category_breakdown,
        "daily_expenses": daily_expenses,
        "biggest_expense": biggest_expense,
    }
