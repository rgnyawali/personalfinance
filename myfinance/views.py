from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import AccountForm, TransactionForm
#from django.utils import timezone
from .models import Account, Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from django.db.models import Q, Count, Sum
import datetime as dt
from django.db.models.functions import ExtractMonth
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.25')



# Create your views here.

def homeview(request):

	return render(request, 'myfinance/home.html',{})

def summary(request):
	dates=Transaction.objects.values('date').distinct()



	allTransactions=Transaction.objects.all().order_by('-date')#[:20]
	incomes = Transaction.objects.filter(Q(category='sa')|Q(category='go')|Q(category='bu')|Q(category='oi'))
	expenses = Transaction.objects.filter(~(Q(category='sa')|Q(category='go')|Q(category='bu')|Q(category='oi')|Q(category='tf'))).order_by('date')
	transfers=Transaction.objects.filter(Q(category='tf'))

	# Last 12 months income & expense summary for creating a chart.
	last12income = Transaction.objects.filter(date__gte=dt.date.today()+relativedelta(months=-12)).filter(Q(category='sa')|Q(category='go')|Q(category='bu')|Q(category='oi'))
	last12expense = Transaction.objects.filter(date__gte=dt.date.today()+relativedelta(months=-12)).filter(~(Q(category='sa')|Q(category='go')|Q(category='bu')|Q(category='oi')|Q(category='tf')))
	
	monthly_income=last12income.values('date__year','date__month').annotate(total_amount=Sum('amount')).order_by('date__year','date__month')
	monthly_expense=last12expense.values('date__year','date__month').annotate(total_amount=Sum('amount')).order_by('date__year','date__month')

	income_dict={dt.datetime(year=t['date__year'],month=t['date__month'],day=1).strftime('%B %Y'):t['total_amount'] for t in monthly_income}
	expense_dict={dt.datetime(year=t['date__year'],month=t['date__month'],day=1).strftime('%B %Y'):t['total_amount'] for t in monthly_expense}
	#monthly_date={dt.datetime(year=t['date__year'],month=t['date__month'],day=1).strftime('%B %Y'):t['total_amount'] for t in tq}
	#print(income_dict)
	#print('################')
	#print(expense_dict)
	#print(last12.objects.aggregate(Sum('amount')))
	#print(myquery)
	#for each in last12:
		#print (f'{each.date}=={each.amount}')
	
	df=pd.DataFrame.from_records(Transaction.objects.all().values_list('date','category','amount'),columns=['date','category','amount'])
	df=df.astype({'date':'datetime64[ns]'})

	df_income=df[df.category.isin(['sa','go','bu','oi'])][['date','amount']]
	df_income.rename(columns={'amount':'income'},inplace=True)
	df_expense=df[~df.category.isin(['sa','go','bu','oi','tf'])][['date','amount']]
	df_expense.rename(columns={'amount':'expense'},inplace=True)
	inc=df_income.groupby(pd.Grouper(key='date', axis=0, freq='ME')).sum()
	exp=df_expense.groupby(pd.Grouper(key='date', axis=0, freq='ME')).sum()
	df2=pd.concat([inc,exp],axis=1)
	df2.fillna(0,inplace=True)
	print(df2.index.month.to_list())
	months=df2.index.strftime("%B %Y").tolist()
	incomes=df2['income'].astype(float).to_list()
	expenses=df2['expense'].astype(float).to_list()
	#print(months,incomes,expenses)
	# Just for trial
	#months=['January','February']
	#incomes=[1200,1250]
	#expenses=[1100,2345]

	



	return render(request,'myfinance/summary.html',{'allTransactions':allTransactions, 'expenses':expenses,'incomes':incomes, 'transfers':transfers, 'dates':dates,
	'months':months,'incomes':incomes,'expenses':expenses})


class TransactionView(View):
	def get(self, request):
		form=TransactionForm()
		return render(request, 'myfinance/transaction.html',{'form':form})

	def post(self, request):
		form=TransactionForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			#print(form.cleaned_data)
			from_account = data.get('tfrom')
			to_account = data.get('tto')

			from_account.balance = from_account.balance - data.get('amount')
			to_account.balance = to_account.balance + data.get('amount')

			from_account.save()
			to_account.save()
			#print(from_account.balance - data.get('amount'))
			#print(to_account.balance + data.get('amount'))


			if data.get('breakdown_option')=='no':
				print('Im at option no')
				i=1
				set_date=data.get('date')
			elif data.get('breakdown_option')=='mm':
				print('im at option multiple month')
				i=data.get('number_month')
				set_date=data.get('start_date')
			elif data.get('breakdown_option')=='my':
				print('im at option multiple years')
				i=data.get('number_year')*12
				set_date=data.get('start_date')
			else:
				print('im at ELSE')
				i=0

			for each in range(i):
				tr=Transaction(tfrom=data.get('tfrom'), 
				   tto=data.get('tto'), 
				   amount=data.get('amount')/i,
				   date=set_date,
				   category=data.get('category'),
				   breakdown_option=data.get('breakdown_option'),
				   number_month=data.get('number_month'),
				   number_year=data.get('number_year'),
				   )
				tr.save()
				set_date=set_date+relativedelta(months=1)

			return redirect(reverse('myfinance:home'))
		return render(request,'myfinance/transaction.html',{'form':form})

class AccountView(View):
	def get(self,request):
		form=AccountForm()
		return render(request, 'myfinance/account.html',{'form':form})

	def post(self,request):
		form=AccountForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('myfinance:home'))
		return render(request,'myfinance/account.html',{'form':form})



