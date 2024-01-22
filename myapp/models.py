from django.contrib.auth.models import User
from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    # Add other category-related fields as needed

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    # Add other tag-related fields as needed

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    tags = models.ManyToManyField(Tag)
    # Add other expense-related fields as needed

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)  # For example, salary, rental income, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.source} - {self.amount}"