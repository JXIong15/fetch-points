# Generated by Django 4.0.1 on 2022-01-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0009_alter_payer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payer',
            name='total_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
