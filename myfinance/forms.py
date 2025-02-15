from django import forms
from .models import Account, Transaction
from django.core.validators import RegexValidator
import datetime as dt


class AccountForm(forms.ModelForm):
	class Meta:
		model=Account 
		exclude=["balance"]
		labels={'account_type':'Type'}
		widgets={'details':forms.Textarea(attrs={'rows':5,'cols':24}), 'track':forms.CheckboxInput(attrs={"class":"form-check form-switch form-check-input","type":"checkbox","role":"switch"})}

class TransactionForm(forms.ModelForm):
	class Meta:
		model=Transaction
		fields="__all__"
		labels={'tfrom':'From',
				'tto':'To',
				'amount':'Amount ($)',
				'date':'Transaction Date',
				'category':'Category',
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

class DownloadRangeForm(forms.Form):
	start_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
	end_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
