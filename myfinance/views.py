from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import AccountForm, TransactionForm
#from django.utils import timezone
from .models import Account, Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from django.db.models import Q


# Create your views here.

def homeview(request):

	return render(request, 'myfinance/home.html',{})

def summary(request):
	dates=Transaction.objects.values('date').distinct()



	allTransactions=Transaction.objects.all().order_by('-date')#[:20]
	incomes = Transaction.objects.filter(Q(category='sa')|Q(category='go')|Q(category='bu')|Q(category='oi'))
	expenses = Transaction.objects.filter(~(Q(category='sa')|Q(category='go')|Q(category='bu')|Q(category='oi')|Q(category='tf'))).order_by('date')
	transfers=Transaction.objects.filter(Q(category='tf'))



	



	return render(request,'myfinance/summary.html',{'allTransactions':allTransactions, 'expenses':expenses,'incomes':incomes, 'transfers':transfers, 'dates':dates})


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



