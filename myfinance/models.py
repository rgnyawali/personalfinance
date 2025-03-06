from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime as dt
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Account(models.Model):
	VENDOR='v'
	OWN='s'
	account_types = [(VENDOR,'Vendor'),
					(OWN,'Self')]
	owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name=models.CharField(max_length=50)
	address=models.CharField(max_length=50, blank=True, null=True)
	balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	account_type=models.CharField(max_length=1,choices=account_types,default=VENDOR)
	details=models.TextField(max_length=100, null=True, blank=True)
	track=models.BooleanField(default=False)

	def __str__(self):
		return (self.name)
	
	def get_absolute_url(self):
		return reverse('account-edit',args=[self.pk])

class Transaction(models.Model):
	HOME_EXPENSES='he' 		# mortgage, insurance
	GROCERY='gr'			# food, cleaning, hygiene
	HOME_IMPROVEMENT='hi'	# furniture, lawn, garden, decoration
	PHONE='ph'				# phone
	UTILITY='ut'			# waste, water, electricity, gas
	INTERNET='in'			# home internet
	FASHION='fa'			# clothing, beauty
	FOODBEVERAGES='fb'		# restaurants
	LIQUOR='lq'				# liquor store, bar
	CAR='cr'				# gas, insurance, loan, maintenance
	MEDICAL='me'			# doctor, medicine
	ENTERTAINMENT='en'		# movies, parties, camping, games
	TRAVEL='tr'				# hotels, car rentals, flights
	CHILDCARE='cc'			# daycare, resp, school fees, swimming, soccer
	EDUCATION='ed'			# tuition, fees, stationary, loan payments
	SUPPORTPAYMENT='sp'		# support payments to parents, children, friends (un-returnable)
	ACCOUNTRECEIVABLE='ar'	# short-term loan (returnable)
	GIFT='gi'
	OTHERS='or'				# Uncategorized, need to open up a category

	SALARY='sa'
	GOVERNMENT='go'
	BUSINESS='bu'
	OTHERINCOME='oi'

	TRANSFER='tf'


	categories = [("Expenses",
					(
					(HOME_EXPENSES,'Home Expenses'),
					  (GROCERY,'Grocery'),
					  (HOME_IMPROVEMENT,'Home Improvement'),
					  (PHONE,'Phone'),
					  (UTILITY,'Utilities'),
					  (INTERNET,'Internet'),
					  (FASHION,'Clothing, Fashion and Accessories'),
					  (FOODBEVERAGES,'Food and Beverages'),
					  (LIQUOR,'Liquor'),
					  (CAR,'Car and Vehicles'),
					  (MEDICAL,'Medical'),
					  (ENTERTAINMENT,'Entertainment'),
					  (TRAVEL,'Travel'),
					  (CHILDCARE,'Child Care'),
					  (EDUCATION,'Education'),
					  (SUPPORTPAYMENT,'Support Payment'),
					  (ACCOUNTRECEIVABLE,'Short Term Lending'),
					  (GIFT,'Gift and Charity'),
					  (OTHERS,'Other Expenses'),
					  ),
					),
				("Income",
					(
					(SALARY,'Salary and Wages'),
					(GOVERNMENT,'Government Support'),
					(BUSINESS,'Business Income'),
					(OTHERINCOME,'Other Income'),
					),
				),
				("Internal Transfer",
	 				(
						 (TRANSFER,'Transfer'),
						 ),
						 
						 )]

	MULTIPLE_YEAR='my'
	MULTIPLE_MONTH='mm'
	NONE='no'

	breakdown_options=[(NONE,'None'),
						(MULTIPLE_MONTH,'Multiple Months'),
						#(SINGLE_CALENDAR_YEAR,'Current Year'),
						#(NEXT_YEAR,'One Year From Now'),
						(MULTIPLE_YEAR,'Multiple Years')]
	
	owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	tfrom=models.ForeignKey('Account',related_name='tfrom', on_delete=models.CASCADE)
	tto=models.ForeignKey('Account',related_name='tto',on_delete=models.CASCADE)
	amount=models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
	date=models.DateField()
	#category=models.CharField(max_length=2,choices=categories, default=GROCERY)
	categorys=models.ForeignKey('Category', related_name='categories', on_delete=models.CASCADE,null=True)
	breakdown_option=models.CharField(max_length=2,choices=breakdown_options, default=NONE)
	start_date=models.DateField(default=dt.datetime.today)
	number_month=models.PositiveIntegerField(default=1)
	number_year=models.PositiveIntegerField(default=1)
	comment=models.TextField(blank=True,null=True)


	def __str__(self):
		return f'{self.tfrom}-->{self.tto}, Date: {self.date:%Y-%m-%d}'
	
	def get_absolute_url(self):
		return reverse('',kwargs={'pk':self.pk})

class Category(models.Model):
	INCOME='I'
	EXPENSES='E'
	TRANSFER='T'
	cat_types=[
		(INCOME,'Income'),
		(EXPENSES,'Expenses'),
		(TRANSFER,'Transfer'),
	]
	owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name=models.CharField(max_length=20)
	cat_type=models.CharField(max_length=1, choices=cat_types, default=INCOME)
	
	def __str__(self):
		return f'{self.name}'
	

