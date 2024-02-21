from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import TagForm, ExpenseForm, IncomeForm
from .models import Tag, Expense, Income, Category
from django.utils.timezone import make_aware
import datetime


class RegisterViewTest(TestCase):
  def test_register_form(self):
    response = self.client.get(reverse('register'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'register.html')
    self.assertIn('form', response.context)
        
    form_data = {
      'username': 'testuser',
      'password1': 'testpassword',
      'password2': 'testpassword'
    }
    response = self.client.post(reverse('register'), data=form_data)
        
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('login'))
        
    self.assertTrue(User.objects.filter(username='testuser').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_login_form(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('form', response.context)
        
        form_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(reverse('login'), data=form_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(reverse('logout'))
        
        self.assertEqual(response.status_code, 302)
        
        self.assertRedirects(response, reverse('home'))
        
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ExpenseFormTest(TestCase):
    def setUp(self):
        # Create a Category instance
        self.category = Category.objects.create(name='Test Category', description='Test description', icon='test')

    def test_expense_form_valid(self):
        form_data = {
            'category': self.category.pk,
            'description': 'Some description',
            'amount': 100,
            'date': make_aware(datetime.datetime(2024, 2, 17)),  # Make the date timezone aware
            # Add any other required fields here
        }
        form = ExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_expense_form_invalid(self):
        form_data = {
            # Incomplete or invalid form data
        }
        form = ExpenseForm(data=form_data)
        self.assertFalse(form.is_valid())


class IncomeFormTest(TestCase):
    def test_income_form_valid(self):
        form_data = {
            'source': 'Some source',
            'amount': 100,
            'date': make_aware(datetime.datetime(2024, 2, 17)),  # Make the date timezone aware
            # Add any other required fields here
        }
        form = IncomeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_income_form_invalid(self):
        form_data = {
            # Incomplete or invalid form data
        }
        form = IncomeForm(data=form_data)
        self.assertFalse(form.is_valid())


class TagFormTest(TestCase):
    def test_tag_form_valid(self):
        form_data = {
            'name': 'Some tag name',
            # Add any other required fields here
        }
        form = TagForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_tag_form_invalid(self):
        form_data = {
            # Incomplete or invalid form data
        }
        form = TagForm(data=form_data)
        self.assertFalse(form.is_valid())


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(user=self.user, name='Test Tag')
        self.expense = Expense.objects.create(user=self.user, category=self.category, description='Test Expense', amount=100, date=datetime.datetime.now())
        self.expense.tags.add(self.tag)
        self.income = Income.objects.create(user=self.user, source='Test Source', amount=100, date=datetime.datetime.now())

    def test_tag_create(self):
        tag_count_before = Tag.objects.count()
        tag = Tag.objects.create(user=self.user, name='New Tag')
        tag_count_after = Tag.objects.count()
        self.assertEqual(tag_count_after, tag_count_before + 1)

    def test_tag_delete(self):
        tag_count_before = Tag.objects.count()
        self.tag.delete()
        tag_count_after = Tag.objects.count()
        self.assertEqual(tag_count_after, tag_count_before - 1)

    def test_tag_update(self):
      new_name = 'Updated Tag'
      self.tag.name = new_name
      self.tag.save()
      updated_tag = Tag.objects.get(id=self.tag.id)
      self.assertEqual(updated_tag.name.lower(), new_name.lower())

    def test_expense_create(self):
        expense_count_before = Expense.objects.count()
        expense = Expense.objects.create(user=self.user, category=self.category, description='New Expense', amount=100, date=datetime.datetime.now())
        expense_count_after = Expense.objects.count()
        self.assertEqual(expense_count_after, expense_count_before + 1)

    def test_expense_delete(self):
        expense_count_before = Expense.objects.count()
        self.expense.delete()
        expense_count_after = Expense.objects.count()
        self.assertEqual(expense_count_after, expense_count_before - 1)

    def test_expense_update(self):
        new_description = 'Updated Expense'
        self.expense.description = new_description
        self.expense.save()
        updated_expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(updated_expense.description, new_description)

    def test_income_create(self):
        income_count_before = Income.objects.count()
        income = Income.objects.create(user=self.user, source='New Source', amount=100, date=datetime.datetime.now())
        income_count_after = Income.objects.count()
        self.assertEqual(income_count_after, income_count_before + 1)

    def test_income_delete(self):
        income_count_before = Income.objects.count()
        self.income.delete()
        income_count_after = Income.objects.count()
        self.assertEqual(income_count_after, income_count_before - 1)

    def test_income_update(self):
        new_source = 'Updated Source'
        self.income.source = new_source
        self.income.save()
        updated_income = Income.objects.get(id=self.income.id)
        self.assertEqual(updated_income.source, new_source)