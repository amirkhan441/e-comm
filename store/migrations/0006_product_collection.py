# Generated by Django 5.2.1 on 2025-05-18 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.CharField(choices=[('summer', 'Summer'), ('winter', 'Winter')], default='summer', max_length=6),
        ),
    ]
