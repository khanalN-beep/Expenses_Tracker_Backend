from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    MonthlyBudgetViewSet, CategoryViewSet, ExpenseViewSet,
    monthly_summary
)

router = DefaultRouter()
router.register("budgets", MonthlyBudgetViewSet, basename="budget")
router.register("categories", CategoryViewSet, basename="category")
router.register("expenses", ExpenseViewSet, basename="expense")

# router.register("budget-detail", MovieBudgetDetailViewSet, basename="budget-detail")
urlpatterns = [
    path("summary/<int:year>/<int:month>/", monthly_summary),
    # path("budget/<int:id>/", MovieBudgetDetailViewSet)
]

urlpatterns += router.urls
