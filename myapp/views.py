from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Value
import calendar
from datetime import *
from .forms import ExpenseForm, IncomeForm, TagForm
from django.http import HttpResponse
from django.utils import timezone
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, is_naive
from django.http import JsonResponse
from django.http import QueryDict


class RegisterView(CreateView):
  form_class = UserCreationForm
  template_name = 'register.html'
  success_url = reverse_lazy('login')

class LoginView(LoginView):
  template_name = 'login.html'
  redirect_authenticated_user = True
  next_page = reverse_lazy('home')

class LogoutView(LogoutView):
  next_page = reverse_lazy('home')


def get_month_days_list(year, month):
  current_year = date.today().year
  current_month = date.today().month
  current_day = date.today().day

  first_day, total_days = calendar.monthrange(year, month)
    
  prev_month = month - 1 if month > 1 else 12
  prev_month_last_day = calendar.monthrange(year if month > 1 else year - 1, prev_month)[1]
  prev_month_days = [{'day': prev_month_last_day - i, 'opacity': 0.3, 'is_current_day': False} for i in range(first_day - 1, 0, -1)]
    
  current_month_days = [{'day': day, 'opacity': 1, 'is_current_day': day == current_day and month == current_month} for day in range(1, total_days + 1)]

  next_month = month + 1 if month < 12 else 1
  next_month_days = [{'day': i, 'opacity': 0.3, 'is_current_day': False} for i in range(1, 35 - len(prev_month_days + current_month_days) + 1, 1)]

  result = prev_month_days + current_month_days + next_month_days
    
  return result

class HomeView(ListView):
  template_name = 'home.html'
  context_object_name = 'transactions'

  def get_queryset(self):
    user = self.request.user

    transactions = []

    if user.is_authenticated:
      expenses = Expense.objects.filter(user=user)
      incomes = Income.objects.filter(user=user)

      transactions = list(expenses) + list(incomes)
      transactions.sort(key=lambda x: x.date, reverse=True)
    
    return transactions[:10]
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      user = self.request.user

      context["financialsummary"] = FinancialSummary.objects.filter(user=user).first() if user.is_authenticated else {'balance': 0, 'total_expenses': 0, 'total_incomes': 0}

      current_year = date.today().year
      current_month = date.today().month
      context["monthdays"] = get_month_days_list(current_year, current_month)

      return context
  

class CategoryListView(ListView):
  model = Category
  template_name = 'category_list.html'
  context_object_name = 'categories'

  def get_queryset(self):
    categories = Category.objects.all()
    user = self.request.user

    if user.is_authenticated:
      # Annotate each category with the count of expenses and the sum of expense amounts
      categories = categories.annotate(
        expense_count = Count('expense', filter=models.Q(expense__user=user)),
        expense_sum = Sum('expense__amount', filter=models.Q(expense__user=user), default=0)
      )
    else:
      categories = categories.annotate(
        expense_count = Value(0),
        expense_sum = Value(0)
      )

    return categories   


class TagListView(ListView):
  model = Tag
  template_name = 'tag_list.html'
  context_object_name = 'tags'

  def get_queryset(self):
        if self.request.user.is_authenticated:
        # Annotate each category with the count of expenses and the sum of expense amounts
          return Tag.objects.filter(user=self.request.user).annotate(
              expense_count = Count('expense'),
              expense_sum = Sum('expense__amount', default=0)
          )
        else:
           return None
  
  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['form'] = TagForm()
     return context


class ExpenseListView(ListView):
  model = Expense
  template_name = 'expense_list.html'
  context_object_name = 'expenses'

  def get_queryset(self):
     if self.request.user.is_authenticated:
        return Expense.objects.filter(user=self.request.user).order_by('-date')
     else:
        return Expense.objects.none()

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['form'] = ExpenseForm()
     return context


class IncomeListView(ListView):
  model = Income
  template_name = 'income_list.html'
  context_object_name = 'incomes'

  def get_queryset(self):
     if self.request.user.is_authenticated:
        return Income.objects.filter(user=self.request.user).order_by('-date')
     else:
        return Income.objects.none()
     
  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['form'] = IncomeForm()
     return context
  



def add_item(request, formClass):
  if not request.user.is_authenticated:
    return JsonResponse({'error': 'User is not authenticated'}, status=403)

  if request.method != 'POST':
    return JsonResponse({'error': 'Method not allowed'}, status=405)
  
  # The two checks above are needed

  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON data'}, status=400)

  #tags = data.get('tags', None)

  form = formClass(data)
  if form.is_valid():
    item = form.save(commit=False)

    item.date = datetime.combine(item.date.date(), timezone.now().time())

    if is_naive(item.date):
      item.date = make_aware(item.date)

    item.user = request.user

    item.save()
    form.save_m2m()
    
    return JsonResponse({'id': item.pk, 'date': item.date}, status=201)
  else:
    return JsonResponse({'error': 'Form data is not valid'}, status=400)
  

def delete_item(request, pk, modelClass):
  if not request.user.is_authenticated:
    return JsonResponse({'error': 'User is not authenticated'}, status=403)
  
  if request.method != 'DELETE':
    return JsonResponse({'error': 'Method not allowed'}, status=405)

  item = get_object_or_404(modelClass, pk=pk)
  if item.user != request.user:
    return JsonResponse({'error': 'User does not have permission to delete this item'}, status=403)
  
  # All three checks above are needed
  
  item.delete()
  return HttpResponse(status=204)


def update_item(request, pk, modelClass, formClass):
  if not request.user.is_authenticated:
    return JsonResponse({'error': 'User is not authenticated'}, status=403)
  
  if request.method != 'PUT':
    return JsonResponse({'error': 'Method not allowed'}, status=405)

  item = get_object_or_404(modelClass, pk=pk)
  if item.user != request.user:
    return JsonResponse({'error': 'User does not have permission to update this item'}, status=403)
  
  # All three checks above are needed

  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON data'}, status=400)
  
  form = formClass(data)
  if form.is_valid():
    updatedItem = form.save(commit=False)
    updatedItem.pk = item.pk
    updatedItem.user = item.user

    if updatedItem.date.date() == item.date.date():
      updatedItem.date = datetime.combine(updatedItem.date.date(), item.date.time())
    else:
      updatedItem.date = datetime.combine(updatedItem.date.date(), timezone.now().time())

    if is_naive(updatedItem.date):
      updatedItem.date = make_aware(updatedItem.date)

    updatedItem.save()
    form.save_m2m()

    return JsonResponse({'date': updatedItem.date}, status=200)
  else:
    return JsonResponse({'error': 'Form data is not valid'}, status=400)
  

def add_tag(request, formClass):
  if not request.user.is_authenticated:
    return JsonResponse({'error': 'User is not authenticated'}, status=403)

  if request.method != 'POST':
    return JsonResponse({'error': 'Method not allowed'}, status=405)
  
  # The two checks above are needed

  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON data'}, status=400)

  form = formClass(data)
  if form.is_valid():
    item = form.save(commit=False)

    item.user = request.user

    item.save()
    form.save_m2m()

    queryset = Tag.objects.filter(user=request.user).annotate(
      expense_count=Count('expense'),
      expense_sum=Sum('expense__amount', default=0)
    )

    # Serialize the queryset to get expense count and sum for the created item
    serialized_item = queryset.filter(pk=item.pk).values('id', 'expense_count', 'expense_sum').first()
    
    return JsonResponse(serialized_item, status=201)
  else:
    return JsonResponse({'error': 'Form data is not valid'}, status=400)
  

def update_tag(request, pk, modelClass, formClass):
  if not request.user.is_authenticated:
    return JsonResponse({'error': 'User is not authenticated'}, status=403)
  
  if request.method != 'PUT':
    return JsonResponse({'error': 'Method not allowed'}, status=405)

  item = get_object_or_404(modelClass, pk=pk)
  if item.user != request.user:
    return JsonResponse({'error': 'User does not have permission to update this item'}, status=403)
  
  # All three checks above are needed

  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON data'}, status=400)
  
  form = formClass(data)
  if form.is_valid():
    updatedItem = form.save(commit=False)
    updatedItem.pk = item.pk
    updatedItem.user = item.user

    updatedItem.save()
    form.save_m2m()

    # Would be 204 (No content) but frontend expects 200
    return JsonResponse({}, status=200)
  else:
    return JsonResponse({'error': 'Form data is not valid'}, status=400)