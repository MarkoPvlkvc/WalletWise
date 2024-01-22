from django.contrib import admin
from .models import *

models = [ExpenseCategory, Tag, Expense, Income]

admin.site.register(models)
