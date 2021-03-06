# Generated by Django 3.2.8 on 2021-11-15 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyVisitors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitors', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Daily Visitors',
                'verbose_name_plural': 'Daily Visitors',
                'db_table': 'daily_visitors',
            },
        ),
        migrations.CreateModel(
            name='NewsLetterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'News Letter Subscriber',
                'verbose_name_plural': 'News Letter Subscriber',
                'db_table': 'news_letter_subscriber',
            },
        ),
        migrations.CreateModel(
            name='TotalVisitors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitors', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Total Visitors',
                'verbose_name_plural': 'Total Visitors',
                'db_table': 'total_visitors',
            },
        ),
        migrations.CreateModel(
            name='RequestProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_datetime', models.DateTimeField(verbose_name='Request Date & Time')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('is_request_proceed', models.BooleanField(default=False, verbose_name='Request Acknowledged/Closed')),
                ('completion_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Completion Date & Time')),
                ('timezone', models.CharField(blank=True, max_length=30, null=True)),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='Remarks')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_product_image_created_by', to='customer.customerprofile', verbose_name='Requested By')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_product_image_customer', to='customer.customerprofile', verbose_name='Customer Details')),
                ('product', models.ForeignKey(limit_choices_to={'is_active': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='request_product_image_product', to='catalogue.product', verbose_name='Product Details')),
                ('product_category', models.ForeignKey(limit_choices_to={'is_active': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='request_product_image_product_category', to='catalogue.category')),
                ('product_collection', models.ForeignKey(blank=True, limit_choices_to={'is_active': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_product_image_product_collection', to='catalogue.collection')),
            ],
            options={
                'verbose_name': 'Request for Additional Image',
                'verbose_name_plural': 'Request for Additional Image',
                'db_table': 'request_product_images',
            },
        ),
        migrations.CreateModel(
            name='ProductRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_views', models.PositiveIntegerField(default=0, verbose_name='Views')),
                ('num_basket_additions', models.PositiveIntegerField(default=0, verbose_name='Basket Additions')),
                ('num_purchases', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Purchases')),
                ('score', models.FloatField(default=0.0, verbose_name='Score')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='catalogue.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Record',
                'verbose_name_plural': 'Product Record',
                'db_table': 'product_records',
                'ordering': ['-num_purchases'],
            },
        ),
        migrations.CreateModel(
            name='CustomerSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_index=True, max_length=255, verbose_name='Search term')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_search_records', to='customer.customerprofile', verbose_name='Customer Details')),
            ],
            options={
                'verbose_name': 'Customer search query',
                'verbose_name_plural': 'Customer search queries',
                'db_table': 'customer_search',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='CustomerProductView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_records_view', to='customer.customerprofile', verbose_name='Customer Details')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'User product view',
                'verbose_name_plural': 'User product views',
                'db_table': 'customer_product_view',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='CustomerProductActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bookmarked', models.BooleanField(default=0)),
                ('is_added_to_cart', models.BooleanField(default=0)),
                ('is_added_to_wishlist', models.BooleanField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_customer_product_activity', to='customer.customerprofile')),
                ('primary_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_customer_product_activity', to='catalogue.product')),
            ],
            options={
                'verbose_name': 'Customer Product Activity',
                'verbose_name_plural': 'Customer Product Activity',
                'db_table': 'customer_product_activity',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bookmarked', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_customer', to='customer.customerprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_product', to='catalogue.product')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_product_category', to='catalogue.category')),
                ('product_collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_product_collection', to='catalogue.collection')),
            ],
            options={
                'verbose_name': 'Bookmark',
                'verbose_name_plural': 'Bookmark',
                'db_table': 'bookmark',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_wishlisted', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_customer', to='customer.customerprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_product', to='catalogue.product')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_product_category', to='catalogue.category')),
                ('product_collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_product_collection', to='catalogue.collection')),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlist',
                'db_table': 'wishlist',
                'unique_together': {('customer', 'product')},
            },
        ),
    ]
