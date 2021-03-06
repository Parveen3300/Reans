# Generated by Django 3.2.8 on 2021-12-01 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_rename_color_product_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_color',
            field=models.CharField(blank=True, choices=[('red', 'red'), ('yellow', 'yellow'), ('blue', 'blue'), ('brown', 'brown'), ('green', 'green'), ('black', 'black'), ('white', 'white')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_size',
            field=models.CharField(blank=True, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=10, null=True),
        ),
    ]
