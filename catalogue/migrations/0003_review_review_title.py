# Generated by Django 3.2.8 on 2021-11-18 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
