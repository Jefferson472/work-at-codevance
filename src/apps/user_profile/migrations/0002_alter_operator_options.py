# Generated by Django 4.1.6 on 2023-02-22 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operator',
            options={'permissions': [('payment_view', 'Can see all payments'), ('payment_create', 'Can create new payments')], 'verbose_name': 'Operator Profile'},
        ),
    ]
