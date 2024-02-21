from django.contrib import admin
from .models import *

models = [Category, Tag, Expense, Income, FinancialSummary]

admin.site.register(models)
