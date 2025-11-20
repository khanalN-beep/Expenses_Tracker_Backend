from django.contrib import admin

from expenses.models import MonthlyBudget, Category, Expense

# Register your models here.
admin.site.register(MonthlyBudget)
admin.site.register(Category)
admin.site.register(Expense)
