from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from expenses.api.v1.serializers import MonthlyBudgetSerializer, CategorySerializer, ExpensesSerializer, \
    MonthlySummarySerializer
from expenses.api.v1.services import calculate_monthly_summary
from expenses.models import MonthlyBudget, Category, Expense


# Create your views here.
class MonthlyBudgetViewSet(viewsets.ModelViewSet):
    serializer_class = MonthlyBudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return MonthlyBudget.objects.none()
        return MonthlyBudget.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    #
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def monthly_summary(request, year, month):
    user = request.user

    try:
        budget = MonthlyBudget.objects.get(user=user, year=year, month=month)
    except MonthlyBudget.DoesNotExist:
        return Response({"error": "Budget not set for this month"}, status=404)

    summary_data = calculate_monthly_summary(user, budget)
    serializer = MonthlySummarySerializer(summary_data)

    return Response(serializer.data)


