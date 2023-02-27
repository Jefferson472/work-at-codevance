# Generated by Django 4.1.6 on 2023-02-24 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('antecipation', '0011_remove_logtransactions_operator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antecipation',
            name='request_antecipation',
        ),
        migrations.AddField(
            model_name='antecipation',
            name='req_antecipation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='antecipation', to='antecipation.requestantecipation'),
        ),
        migrations.AlterField(
            model_name='requestantecipation',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='req_antecipation', to='payment.payment'),
        ),
    ]