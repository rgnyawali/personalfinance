from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'myfinance'

urlpatterns = [
    path('', views.homeview, name='home'),
    path('transaction/',views.TransactionView.as_view(),name='transaction'),
    path('vendor/',views.AccountView.as_view(),name='vendor'),
    path('summary/',views.summary, name='summary'),
    path('createaccount/',views.CreateAccount.as_view(),name='createaccount'),
    path('listaccount/',views.AccountListView.as_view(),name='account-list'),
    path('edit/<int:pk>',views.AccountUpdateView.as_view(),name='account-edit'),
    #path('summary/<int:year>',views.yearly_summary,name='yearly_summary'),
    #path('summary/<int:year>/<int:month>',views.monthly_summary,name='monthly_summary'),
    #path('transaction-detail/<int:pk>', views.transaction),

    path('details/<str:detail>', views.details, name='details'),
]