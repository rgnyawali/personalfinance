from .models import Account, Transaction, Category
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from django.utils import timezone


def get_data(owner):
    #INCOME_CATEGORY=['sa','go','bu','oi']
    icats=Category.objects.filter(owner=owner).filter(cat_type='I')
    INCOME_CATEGORY=[each.pk for each in icats]
    INCOME_LABELS=[each.name for each in icats]

    ecats=Category.objects.filter(owner=owner).filter(cat_type='E')
    EXPENSE_CATEGORY=[each.pk for each in ecats]
    EXPENSE_LABELS=[each.name for each in ecats]
    #EXPENSE_CATEGORY=['he', 'gr','hi','ph','ut','in','fa','fb','lq','cr','me','en','tr','cc','ed','sp','ar','gi','or']

    # Last 12 months income & expense summary (Line chart)
    df=pd.DataFrame.from_records(Transaction.objects.filter(owner=owner).filter(date__gte=dt.date.today()+relativedelta(months=-12)).filter(date__lte=dt.date.today()).values_list('date','categorys','amount'),columns=['date','category','amount'])
    df=df.astype({'date':'datetime64[ns]'})

    df_income=df[df.category.isin(INCOME_CATEGORY)][['date','amount']]
    df_income.rename(columns={'amount':'income'},inplace=True)
    df_expense=df[df.category.isin(EXPENSE_CATEGORY)][['date','amount']]
    df_expense.rename(columns={'amount':'expense'},inplace=True)
    inc=df_income.groupby(pd.Grouper(key='date', axis=0, freq='ME')).sum()
    exp=df_expense.groupby(pd.Grouper(key='date', axis=0, freq='ME')).sum()
    df2=pd.concat([inc,exp],axis=1)
    df2.fillna(0,inplace=True)
    month12=df2.index.strftime("%b %Y").tolist()
    month6=df2[-6:].index.strftime("%b %Y").tolist()

    income12=df2['income'].astype(float).to_list()
    income6=df2[-6:]['income'].astype(float).to_list()

    expense12=df2['expense'].astype(float).to_list()
    expense6=df2[-6:]['expense'].astype(float).to_list()

    # Current Month Expense by category (Pie chart)
    current_month=timezone.now().month

    df3=df[(df.date.dt.month==current_month)&(df.category.isin(EXPENSE_CATEGORY))][['amount','category']]
    df4=df3.groupby(pd.Grouper(key='category')).sum()
    expense_label=df4.index.to_list()
    exp_label = list(Category.objects.filter(pk__in=expense_label).values_list('name', flat=True))

    expense_data=df4['amount'].astype(float).to_list()

    #expense_label_dict=dict(Transaction.categories[0][1])
    #expense_label=EXPENSE_CATEGORY #[expense_label_dict[each] for each in expense_label]

    cur_month_expenses = {
        'labels': exp_label,
        'data': expense_data, 
    }


    # Current Month Income by category (Pie chart)
    df5=df[(df.date.dt.month==current_month)&(df.category.isin(INCOME_CATEGORY))][['amount','category']]
    df6=df5.groupby(pd.Grouper(key='category')).sum()
    income_label=df6.index.to_list()
    inc_label = list(Category.objects.filter(pk__in=income_label).values_list('name', flat=True))
    income_data=df6['amount'].astype(float).to_list()

    #income_label_dict=dict(Transaction.categories[1][1])
    #income_label= INCOME_LABELS #[income_label_dict[each] for each in income_label]
    #print([x for x in income_label)
    cur_month_income = {
        'labels': inc_label,
        'data': income_data,
    }

    x_expense=df[df.category.isin(EXPENSE_CATEGORY)]
    x_expense['month']=x_expense['date'].dt.to_period('M')
    pivot_df=x_expense.pivot_table(index='month',columns='category',values='amount',aggfunc='sum',fill_value=0)
    pivot_df=pivot_df.reset_index()
    month_list = pivot_df['month'].dt.strftime('%b %Y').tolist()

    #expense_dict={}
    #for cols in pivot_df.columns:
        #if cols != 'month':
            #expense_dict[expense_label_dict[cols]]=pivot_df[cols].astype(float).to_list()
    cur_month=timezone.now().strftime("%B")
    #print(month12)
    return (cur_month, month12, month6, income12, income6, expense12, expense6, expense_data, expense_label, income_data, income_label, cur_month_expenses, cur_month_income)

def get_detail_data(n, owner):
    #INCOME_CATEGORY=['sa','go','bu','oi']
    #EXPENSE_CATEGORY=['he', 'gr','hi','ph','ut','in','fa','fb','lq','cr','me','en','tr','cc','ed','sp','ar','gi','or']
    icats=Category.objects.filter(owner=owner).filter(cat_type='I')
    INCOME_CATEGORY=[each.pk for each in icats]
    INCOME_LABELS=[each.name for each in icats]

    ecats=Category.objects.filter(owner=owner).filter(cat_type='E')
    EXPENSE_CATEGORY=[each.pk for each in ecats]
    EXPENSE_LABELS=[each.name for each in ecats]

    df=pd.DataFrame.from_records(Transaction.objects.filter(owner=owner).filter(date__gte=dt.date.today()+relativedelta(months=-n)).filter(date__lte=dt.date.today()).values_list('date','category','amount'),columns=['date','category','amount'])
    df=df.astype({'date':'datetime64[ns]'})

    x_expense=df[df.category.isin(EXPENSE_CATEGORY)]
    x_expense['month']=x_expense['date'].dt.to_period('M')
    pivot_df=x_expense.pivot_table(index='month',columns='category',values='amount',aggfunc='sum',fill_value=0)
    pivot_df=pivot_df.reset_index()
    month_expense_list = pivot_df['month'].dt.strftime('%b %Y').tolist()
    
    expense_label_dict=dict(Transaction.categories[0][1])

    expense_dict={}
    for cols in pivot_df.columns:
        if cols != 'month':
            expense_dict[expense_label_dict[cols]]=pivot_df[cols].astype(float).to_list()
    
    edf=pd.DataFrame.from_dict(expense_dict)
    edf.set_index([month_expense_list],inplace=True)
    expense_table=edf.iloc[::-1].to_html(justify='center',classes="table table-bordered align-middle text-center font-responsive text-white", float_format=lambda x: f"{x:,.2f}")


    x_income=df[df.category.isin(INCOME_CATEGORY)]
    x_income['month']=x_income['date'].dt.to_period('M')
    pivot_df2=x_income.pivot_table(index='month',columns='category',values='amount',aggfunc='sum',fill_value=0)
    pivot_df2=pivot_df2.reset_index()
    month_income_list = pivot_df2['month'].dt.strftime('%b %Y').tolist()
    
    income_label_dict=dict(Transaction.categories[1][1])

    income_dict={}
    for cols in pivot_df2.columns:
        if cols != 'month':
            income_dict[income_label_dict[cols]]=pivot_df2[cols].astype(float).to_list()

    idf=pd.DataFrame.from_dict(income_dict)
    idf.set_index([month_income_list], inplace=True)
    income_table=idf.iloc[::-1].to_html(justify='center',classes="table table-bordered align-middle text-center font-responsive text-white", float_format=lambda x: f"{x:,.2f}")




    return(month_expense_list, expense_dict, month_income_list, income_dict, income_table, expense_table)


