from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import AccountForm, TransactionForm, DownloadRangeForm, AccountChangeForm
from django.utils import timezone
from .models import Account, Transaction, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from django.db.models import Q, Count, Sum
import datetime as dt
from django.db.models.functions import ExtractMonth
import pandas as pd
import numpy as np
from .script import get_data, get_detail_data
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
#np.set_printoptions(legacy='1.25')



# Create your views here.

def homeview(request):
	return render(request, 'myfinance/home.html',{})

@login_required
def details(request, detail):
	owner=request.user
	month4_list, expense4_dict, month4_income_list, income4_dict, income_table, expense_table = get_detail_data(4,owner)
	month12_list, expense12_dict, month12_income_list, income12_dict, _ , _ = get_detail_data(12,owner)
	ctx={'detail':detail,'month6_list':month4_list,'expense6_dict':expense4_dict,'month12_list':month12_list,'expense12_dict':expense12_dict, 
		'month4_income_list':month4_income_list,'income4_dict':income4_dict,'month12_income_list':month12_income_list,'income12_dict':income12_dict,'income_table':income_table,
		'expense_table':expense_table}
	return render(request, 'myfinance/details.html',ctx)

@login_required
def summary(request):
	owner=request.user
	cur_month, month12, month6, income12, income6, expense12, expense6, expense_data, expense_label, income_data, income_label, cur_month_expenses, cur_month_income = get_data(owner)
	allTransactions=Transaction.objects.filter(owner=request.user).order_by('-date')[:50]
	tracked_accounts=Account.objects.filter(owner=request.user).filter(track=True)
	#print(tracked_accounts)

	if request.method=='POST':
		form=DownloadRangeForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']

			data=Transaction.objects.filter(owner=request.user).filter(date__range=[start_date,end_date])

			response=HttpResponse(content_type='text/csv')
			response['Content-Disposition']='attachment; filename="transaction.csv"'

			writer=csv.writer(response)
			writer.writerow(['Date','From','To','Amount','Comment'])
			for each in data:
				writer.writerow([each.date, each.tfrom, each.tto, each.amount, each.comment])
			
			return response
	form=DownloadRangeForm()
	return render(request,'myfinance/summary.html',{'allTransactions':allTransactions,'tracked_accounts':tracked_accounts,'cur_month':cur_month,'months':month12,'incomes':income12,'expenses':expense12,
														'cur_month_expenses':cur_month_expenses,'cur_month_income':cur_month_income,'form':form})


class TransactionView(LoginRequiredMixin, View):
	def get(self, request):
		form=TransactionForm(owner=self.request.user)
		return render(request, 'myfinance/transaction.html',{'form':form})

	def post(self, request):
		form=TransactionForm(request.POST,owner=self.request.user)
		if form.is_valid():
			data=form.cleaned_data
			owner=request.user
			from_account = data.get('tfrom')
			to_account = data.get('tto')

			from_account.balance = from_account.balance - data.get('amount')
			to_account.balance = to_account.balance + data.get('amount')

			from_account.owner=owner
			to_account.owner=owner

			from_account.save()
			to_account.save()

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
				tr=Transaction(owner=owner,
					tfrom=data.get('tfrom'), 
				   tto=data.get('tto'), 
				   amount=data.get('amount')/i,
				   date=set_date,
				   #categorys=data.get('category'),
				   categorys=data.get('categorys'),
				   breakdown_option=data.get('breakdown_option'),
				   number_month=data.get('number_month'),
				   number_year=data.get('number_year'),
				   )
				tr.save()
				set_date=set_date+relativedelta(months=1)

			return redirect(reverse('myfinance:home'))
		return render(request,'myfinance/transaction.html',{'form':form})

class AccountView(LoginRequiredMixin,View):
	def get(self,request):
		return render(request, 'myfinance/account.html',{})


class CreateAccount(LoginRequiredMixin,View):
	def get(self,request):
		form = AccountForm()
		return render(request, 'myfinance/createaccount.html',{'form':form})

	def post(self,request):
		form=AccountForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.owner=self.request.user
			obj.save()
			return redirect(reverse('myfinance:home'))
		return render(request,'myfinance/createaccount.html',{'form':form})

class AccountListView(ListView):
	model=Account
	template_name='myfinance/account_list.html'
	context_object_name='accounts'

	def get_queryset(self):
		return Account.objects.filter(owner=self.request.user)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountChangeForm
    template_name = 'myfinance/account_edit_form.html'
    success_url = reverse_lazy('myfinance:account-list')
    
    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_types'] = Account.account_types
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('HX-Request'):
            # Return just the updated account item HTML
            return render(self.request, 'myfinance/account_list_item.html', {'account': self.object})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            return render(self.request, self.template_name, {
                'form': form, 
                'account': self.get_object(),
                'account_types': Account.account_types
            })
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.headers.get('HX-Request'):
            return render(request, self.template_name, {
                'account': self.object,
                'account_types': Account.account_types
            })
        return super().get(request, *args, **kwargs)
