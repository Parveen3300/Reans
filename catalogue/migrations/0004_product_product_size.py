# Generated by Django 3.2.8 on 2021-11-18 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_review_review_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=1, null=True),
        ),
    ]
