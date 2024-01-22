from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class RegisterView(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'register.html'

class LoginView(LoginView):
  template_name = 'login.html'
  redirect_authenticated_user = True
  next_page = reverse_lazy('home')

class LogoutView(LogoutView):
  next_page = reverse_lazy('home')


class ExpenseCategoryListView(ListView):
  model = ExpenseCategory
  template_name = 'expensecategory_list.html'
  context_object_name = 'expensecategories'

class TagListView(ListView):
  model = Tag
  template_name = 'tag_list.html'
  context_object_name = 'tags'

class ExpenseListView(ListView):
  model = Expense
  template_name = 'expense_list.html'
  context_object_name = 'expenses'

class IncomeListView(ListView):
  model = Income
  template_name = 'income_list.html'
  context_object_name = 'incomes'
