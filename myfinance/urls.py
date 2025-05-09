from django.contrib import admin
from django.urls import path, include
from . import views
from .views import UserSummaryView

app_name = 'myfinance'

urlpatterns = [
    path('', views.homeview, name='home'),
    path('transaction/',views.TransactionView.as_view(),name='transaction'),
    path('vendor/',views.AccountView.as_view(),name='vendor'),
    path('summary/',views.summary, name='summary'),
    path('settings/',views.settings, name='settings'),

    #==== Vendor Account List, Create and Edit
    path('createaccount/',views.CreateAccount.as_view(),name='createaccount'),
    path('listaccount/',views.AccountListView.as_view(),name='account-list'),
    path('edit/<int:pk>',views.AccountUpdateView.as_view(),name='account-edit'),

    #=== Category List, Create and Edit
    path('createcategory/',views.CreateCategory.as_view(),name='category-create'), #CreateCategory
    path('listcategory/',views.CategoryListView.as_view(),name='category-list'),
    path('editcategory/<int:pk>',views.CategoryUpdateView.as_view(),name='category-edit'), #CategoryUpdateView

    #=== Transaction List and Edit
    path('listtransaction/',views.TransactionListView.as_view(),name='transaction-list'),
    path('edittransaction/<int:pk>',views.TransactionUpdateView.as_view(),name='transaction-edit'),

    path('user-summary/', UserSummaryView.as_view(), name='user-summary'),
    path('details/<str:detail>', views.details, name='details'),
]