# Generated by Django 5.0 on 2024-01-14 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royalbankapp', '0007_rename_timestamp_transaction_timedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='Timedata',
            field=models.CharField(max_length=100),
        ),
    ]