# Generated by Django 4.0.1 on 2022-01-13 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0006_alter_spend_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spend',
            name='receipt',
            field=models.JSONField(),
        ),
    ]