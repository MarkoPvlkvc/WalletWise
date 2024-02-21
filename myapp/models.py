from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    icon = models.TextField(max_length=20, default='app')
    # Add other category-related fields as needed

    def __str__(self):
        return self.name

def validate_tag_name(value):
    if ';' in value:
        raise ValidationError("Tag name cannot contain the character ';'.")
  
class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    # Add other tag-related fields as needed

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()  # Capitalize the first letter
        super(Tag, self).save(*args, **kwargs)
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag, blank=True)
    # Add other expense-related fields as needed

    def __str__(self):
        return f"{self.description} - {self.amount}"
    
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)  # For example, salary, rental income, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.source} - {self.amount}"
    
class FinancialSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_incomes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

@receiver(post_save, sender=Expense)
@receiver(post_save, sender=Income)
@receiver(post_delete, sender=Expense)
@receiver(post_delete, sender=Income)
def update_summary(sender, instance, **kwargs):
    # Update the financial summary model when a new expense or income is added
    user = instance.user
    expenses_total = Expense.objects.filter(user=user).aggregate(models.Sum('amount'))['amount__sum'] or 0
    incomes_total = Income.objects.filter(user=user).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    summary, created = FinancialSummary.objects.get_or_create(user=user)
    summary.total_expenses = expenses_total
    summary.total_incomes = incomes_total
    summary.balance = incomes_total - expenses_total
    summary.save()