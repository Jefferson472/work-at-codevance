# Generated by Django 4.1.6 on 2023-02-22 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_operator_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operator',
            options={'permissions': [('payment_view', 'Can see all payments'), ('payment_create', 'Can create new payments'), ('antecipation_request_review', 'Can approve or reprove a antecipation request')], 'verbose_name': 'Operator Profile'},
        ),
    ]
