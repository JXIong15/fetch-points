# Generated by Django 4.0.1 on 2022-01-12 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0003_spend_alter_transaction_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='spend',
            name='receipt',
            field=models.TextField(blank=True, null=True),
        ),
    ]
