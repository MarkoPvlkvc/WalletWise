from django import forms
from .models import Tag, Expense, Income


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }


class IncomeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']