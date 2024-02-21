import factory
from factory.django import DjangoModelFactory
from .models import Tag, Expense, Income, Category
import random
from decimal import Decimal

class TagFactory(DjangoModelFactory):
  class Meta:
    model = Tag

  user = 1
  name = factory.Sequence(lambda n: f'tag {n}')

class ExpenseFactory(DjangoModelFactory):
  class Meta:
    model = Expense

  user = 1
  description = factory.Sequence(lambda n: f'expense {n}')
  amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, max_value=5000)
  date = factory.Faker('date_time')

  @classmethod
  def _create(cls, model_class, *args, **kwargs):
    category = random.choice(Category.objects.all())
    kwargs['category'] = category
    return super()._create(model_class, *args, **kwargs)

class IncomeFactory(DjangoModelFactory):
  class Meta:
    model = Income

  user = 1
  source = factory.Sequence(lambda n: f'income {n}')
  amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, min_value=6000, max_value=10000)
  date = factory.Faker('date_time')