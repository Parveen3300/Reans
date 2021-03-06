# Generated by Django 3.2.8 on 2021-11-15 05:11

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('offer_price_type', models.CharField(choices=[('PERCENTAGE', 'PERCENTAGE'), ('RUPPPEES', 'INR')], default='PERCENTAGE', max_length=128)),
                ('offer_type', models.CharField(choices=[('offer', 'Offer'), ('Voucher', 'Voucher')], default='offer', max_length=128)),
                ('value', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_location_applicable', models.BooleanField(default=0)),
                ('city', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='state', chained_model_field='state', db_column='city', limit_choices_to={'is_active': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_offers', show_all=True, to='location.citymaster')),
                ('country', models.ForeignKey(blank=True, db_column='country', limit_choices_to={'is_active': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_offers', to='location.countrymaster')),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_offers', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('included_products', models.ManyToManyField(related_name='includes', to='catalogue.Product')),
                ('state', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='country', chained_model_field='country', db_column='state', limit_choices_to={'is_active': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_offers', show_all=True, to='location.statemaster')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_offers', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Offer',
                'verbose_name_plural': 'Offers',
                'db_table': 'product_offers',
            },
        ),
        migrations.CreateModel(
            name='VoucherSetConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('count', models.PositiveIntegerField(verbose_name='Number of vouchers')),
                ('code_length', models.IntegerField(default=12, verbose_name='Length of Code')),
                ('description', models.TextField(verbose_name='Description')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('start_datetime', models.DateTimeField(verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='End datetime')),
            ],
            options={
                'verbose_name': 'Voucher Set Configuration',
                'verbose_name_plural': 'Voucher Set Configurations',
                'ordering': ['-date_created'],
                'get_latest_by': 'date_created',
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_type', models.CharField(choices=[('Percentage', '%'), ('Ruppees', 'INR')], default='Ruppees', max_length=15)),
                ('name', models.CharField(help_text='This will be shown in the checkout and basket once the voucher is entered', max_length=128, unique=True, verbose_name='Name')),
                ('code', models.CharField(db_index=True, help_text='Case insensitive / No spaces allowed', max_length=128, unique=True, verbose_name='Code')),
                ('usage', models.CharField(choices=[('Single use', 'Can be used once by one customer'), ('Multi-use', 'Can be used multiple times by multiple customers'), ('Once per customer', 'Can only be used once per customer')], default='Multi-use', max_length=128, verbose_name='Usage')),
                ('start_datetime', models.DateTimeField(db_index=True, verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(db_index=True, verbose_name='End datetime')),
                ('num_basket_additions', models.PositiveIntegerField(default=0, verbose_name='Times added to basket')),
                ('num_orders', models.PositiveIntegerField(default=0, verbose_name='Times on orders')),
                ('total_discount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Total discount')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('offers', models.ManyToManyField(limit_choices_to={'offer_type': 'Voucher'}, related_name='vouchers', to='offer_coupon_voucher.Offer', verbose_name='Offers')),
                ('voucher_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='offer_coupon_voucher.vouchersetconfiguration')),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
                'ordering': ['-date_created'],
                'get_latest_by': 'date_created',
            },
        ),
    ]
