# Generated by Django 3.2.8 on 2021-12-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
