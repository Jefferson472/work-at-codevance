# Generated by Django 4.1.6 on 2023-02-22 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('antecipation', '0006_logtransactions_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestantecipation',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='anticipation', to='payment.payment'),
        ),
    ]
