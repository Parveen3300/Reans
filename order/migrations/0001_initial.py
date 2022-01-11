# Generated by Django 3.2.8 on 2021-11-15 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basket', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Order number')),
                ('currency', models.CharField(default='INR', max_length=12, verbose_name='Currency')),
                ('total_incl_tax', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Order total (inc. tax)')),
                ('total_excl_tax', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Order total (excl. tax)')),
                ('shipping_incl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Shipping charge (inc. tax)')),
                ('shipping_excl_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Shipping charge (excl. tax)')),
                ('shipping_method', models.CharField(blank=True, max_length=128, null=True, verbose_name='Shipping method')),
                ('shipping_code', models.CharField(blank=True, default='', max_length=128)),
                ('status', models.CharField(blank=True, max_length=100, verbose_name='Status')),
                ('guest_email', models.EmailField(blank=True, max_length=254, verbose_name='Guest email address')),
                ('date_placed', models.DateTimeField(db_index=True)),
                ('basket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basket.basket', verbose_name='Basket')),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_billing_address', to='customer.customeraddress', verbose_name='Billing Address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_user', to='customer.customerprofile', verbose_name='User')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_shipping_address', to='customer.customeraddress', verbose_name='Shipping Address')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-date_placed'],
            },
        ),
    ]