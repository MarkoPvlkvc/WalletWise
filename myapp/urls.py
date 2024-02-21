from django.urls import path
from .views import *
from .forms import IncomeForm, ExpenseForm, TagForm
from .models import Tag, Expense, Income

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('categories/', CategoryListView.as_view(), name='categories'),

    path('tags/', TagListView.as_view(), name='tags'),
    path('tags/add/', lambda request: add_tag(request, TagForm), name='add-tag'),
    path('tags/delete/<int:pk>/', lambda request, pk: delete_item(request, pk, Tag), name='delete-tag'),
    path('tags/update/<int:pk>/', lambda request, pk: update_tag(request, pk, Tag, TagForm), name='update-tag'),

    path('expenses/', ExpenseListView.as_view(), name='expenses'),
    path('expenses/add/', lambda request: add_item(request, ExpenseForm), name='add-expense'),
    path('expenses/delete/<int:pk>/', lambda request, pk: delete_item(request, pk, Expense), name='delete-expense'),
    path('expenses/update/<int:pk>/', lambda request, pk: update_item(request, pk, Expense, ExpenseForm), name='update-expense'),
    
    path('incomes/', IncomeListView.as_view(), name='incomes'),
    path('incomes/add/', lambda request: add_item(request, IncomeForm), name='add-income'),
    path('incomes/delete/<int:pk>/', lambda request, pk: delete_item(request, pk, Income), name='delete-income'),
    path('incomes/update/<int:pk>/', lambda request, pk: update_item(request, pk, Income, IncomeForm), name='update-income'),
]
