import random

from django.db import transaction
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from ...models import Tag, Expense, Income
from ...factory import TagFactory, ExpenseFactory, IncomeFactory

NUM_INSTANCES = 5

class Command(BaseCommand):
  help = 'Generate test data for Tag, Expense, and Income models.'

  @transaction.atomic
  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS('Deleting old data...'))
    Tag.objects.all().delete()
    Expense.objects.all().delete()
    Income.objects.all().delete()

    self.stdout.write(self.style.SUCCESS('Creating new data...'))

    user = User.objects.get(pk=1)

    # Create tags
    for _ in range(NUM_INSTANCES):
      TagFactory(user=user)

    # Create expenses
    for _ in range(NUM_INSTANCES):
      expense = ExpenseFactory(user=user)
      # Add random tags to each expense
      tags = Tag.objects.filter(user=user)
      expense.tags.set(random.sample(list(tags), k=random.randint(1, NUM_INSTANCES)))

    # Create incomes
    for _ in range(NUM_INSTANCES):
      IncomeFactory(user=user)

    self.stdout.write(self.style.SUCCESS(f'Created {NUM_INSTANCES} instances for each model.'))
