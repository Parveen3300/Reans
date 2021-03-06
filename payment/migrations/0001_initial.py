# Generated by Django 3.2.8 on 2021-11-15 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import payment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuration', '0001_initial'),
        ('customer', '0001_initial'),
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethodConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('pay_pal_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment Id')),
                ('pay_pal_name', models.CharField(blank=True, max_length=255, null=True)),
                ('credit_card_type', models.CharField(blank=True, max_length=50, null=True)),
                ('credit_card_no', models.BigIntegerField(verbose_name='Card Number')),
                ('cvv_no', models.IntegerField(blank=True, null=True, verbose_name='CVV Number')),
                ('expiry_date', models.DateTimeField(auto_now_add=True)),
                ('expiry_year', models.IntegerField(blank=True, null=True)),
                ('expiry_month', models.IntegerField(blank=True, null=True)),
                ('card_name', models.CharField(blank=True, max_length=35, null=True, verbose_name='Card Name')),
                ('default_payment_method', models.IntegerField(blank=True, null=True, verbose_name='Default Payment card Number')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_paymentmethodconfigurations', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile_payment_method', to='customer.customerprofile', verbose_name='Company Details')),
            ],
            options={
                'verbose_name': '      Payment Card Details',
                'verbose_name_plural': '     Payment Card Details',
            },
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Invoice No.')),
                ('payment_datetime', models.DateTimeField(auto_now_add=True)),
                ('amount_type', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', payment.models.MinMaxFloat(blank=True, default=0, null=True, verbose_name='Amount (in $)')),
                ('initiated_by', models.CharField(blank=True, max_length=100, null=True, verbose_name='Initiated By')),
                ('payment_status', models.CharField(blank=True, max_length=150, null=True, verbose_name='Payment Status')),
                ('payment_status_count', models.CharField(blank=True, max_length=150, null=True, verbose_name='Payment Status Count')),
                ('is_active', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=50, null=True, verbose_name='Transaction Payment ID')),
                ('payment_gateway_amount', payment.models.MinMaxFloat(blank=True, default=0, null=True, verbose_name='Gate way Amount (in $)')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuration.currencymaster', verbose_name='Currency Details')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile_payment_transaction', to='customer.customerprofile', verbose_name='Company Details')),
                ('order_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_order_customer_transaction', to='order.order')),
                ('payment_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile_payment_option', to='payment.paymentmethodconfiguration', verbose_name='Company Payment Type')),
            ],
            options={
                'verbose_name': '    Company Payment Transaction History',
                'verbose_name_plural': '    Company Payment Transaction History',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethodOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('payment_methods_name', models.CharField(max_length=30)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_paymentmethodoptions', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_paymentmethodoptions', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': '      Payment Methods Option',
                'verbose_name_plural': '      Payment Methods Option',
            },
        ),
        migrations.AddField(
            model_name='paymentmethodconfiguration',
            name='payment_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_payment_option', to='payment.paymentmethodoption', verbose_name='Payment Method Name'),
        ),
        migrations.AddField(
            model_name='paymentmethodconfiguration',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_paymentmethodconfigurations', to=settings.AUTH_USER_MODEL, verbose_name='Updated By'),
        ),
    ]
