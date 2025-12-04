import calendar

from rest_framework import serializers

from expenses.models import MonthlyBudget, Expense, Category


class MonthlyBudgetSerializer(serializers.ModelSerializer):
    month_name = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyBudget
        fields = '__all__'
        read_only_fields = ('user',)

    def get_month_name(self, obj):
        return calendar.month_name[obj.month]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('user',)


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('user',)

class MonthlySummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    monthly_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit_or_loss = serializers.CharField()
    percentage = serializers.FloatField()
    category_breakdown = serializers.DictField(
        child=serializers.DecimalField(max_digits=12, decimal_places=2)
    )

    daily_expenses = serializers.ListField()

    biggest_expense = serializers.DictField()