from django.contrib.auth.models import User
from django.db import models

from expensetracker import settings


# Create your models here.
class MonthlyBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f"{self.month}/{self.year} - {self.user.username}"


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Expense(models.Model):
    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('bank', 'Bank / Bank Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(MonthlyBudget, on_delete=models.SET_NULL, null=True ,related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.title}"


class Income(models.Model):
    INCOME_CATEGORIES = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('business', 'Business'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=INCOME_CATEGORIES, default='salary')






