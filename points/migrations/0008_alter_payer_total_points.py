# Generated by Django 4.0.1 on 2022-01-13 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0007_alter_spend_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payer',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
    ]