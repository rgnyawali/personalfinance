# Generated by Django 5.1 on 2025-02-14 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfinance', '0006_alter_transaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('Expenses', [('he', 'Home Expenses'), ('gr', 'Grocery'), ('hi', 'Home Improvement'), ('ph', 'Phone'), ('ut', 'Utilities'), ('in', 'Internet'), ('fa', 'Clothing, Fashion and Accessories'), ('fb', 'Food and Beverages'), ('lq', 'Liquor'), ('cr', 'Car and Vehicles'), ('me', 'Medical'), ('en', 'Entertainment'), ('tr', 'Travel'), ('cc', 'Child Care'), ('ed', 'Education'), ('sp', 'Support Payment'), ('ar', 'Short Term Lending'), ('gi', 'Gift and Charity'), ('or', 'Other Expenses')]), ('Income', [('sa', 'Salary and Wages'), ('go', 'Government Support'), ('bu', 'Business Income'), ('oi', 'Other Income')]), ('Internal Transfer', [('tf', 'Transfer')])], default='gr', max_length=2),
        ),
    ]
