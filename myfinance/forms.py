from django import forms
from .models import Account, Transaction, Category
from django.core.validators import RegexValidator
import datetime as dt


class AccountForm(forms.ModelForm):
	class Meta:
		model=Account 
		exclude=["balance",'owner']
		labels={'account_type':'Type'}
		widgets={'details':forms.Textarea(attrs={'rows':5,'cols':24}), 'track':forms.CheckboxInput(attrs={"class":"form-check form-check-input","type":"checkbox","role":"switch"})}

class TransactionForm(forms.ModelForm):
	class Meta:
		model=Transaction
		#fields="__all__"
		exclude=['owner',]
		labels={'tfrom':'From',
				'tto':'To',
				'amount':'Amount ($)',
				'date':'Transaction Date',
				#'category':'Category',
				'categorys':'Category 2',
				'breakdown_option':'Breakdown',
				'start_date':'Start Date',
				'number_month':'Number of Months',
				'number_year': 'Number of Years',
				'comment': 'Comments',
				#'month_start':'Month Start',
				#'month_end':'Month End',
				#'year_start':'Year Start',
				#'year_end':'Year End'
				}
		widgets={'date':forms.DateInput(attrs={'type':'date'}),
				'start_date':forms.DateInput(attrs={'type':'date'}),
				'number_month':forms.TextInput(attrs={'type':'number'}),
				'number_year':forms.TextInput(attrs={'type':'number'}),
				'breakdown_option':forms.Select(attrs={'onchange':'hideMonth()'})
				}
	def __init__(self, *args, **kwargs):
		print('****************************')
		user = kwargs.pop('owner', None)  # Extract user from kwargs
		print(user.email)
		super().__init__(*args, **kwargs)
        
		if user:
			self.fields['tfrom'].queryset = Account.objects.filter(owner=user)
			self.fields['tto'].queryset = Account.objects.filter(owner=user)
			#self.fields['categorys'].queryset = Category.objects.filter(owner=user)
			
			# Here is the display categorization of Categorys
			categories = Category.objects.filter(owner=user).order_by('cat_type')  # Assuming category field exists
			grouped_choices = {}
			for category in categories:
				grouped_choices.setdefault(Category.category, []).append((category.id, category.name))  # (ID, Label)
			self.fields['categorys'].choices = self._get_grouped_choices(grouped_choices)
            #self.fields['account2'].choices = self._get_grouped_choices(grouped_choices)

	def _get_grouped_choices(self, grouped_choices):
		return [(category, choices) for category, choices in grouped_choices.items()]

class DownloadRangeForm(forms.Form):
	start_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
	end_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

class AccountChangeForm(forms.ModelForm):
	class Meta:
		model=Account
		#fields='__all__'
		exclude=['owner',]