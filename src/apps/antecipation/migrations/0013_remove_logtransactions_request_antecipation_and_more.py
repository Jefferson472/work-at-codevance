# Generated by Django 4.1.6 on 2023-02-27 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antecipation', '0012_remove_antecipation_request_antecipation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logtransactions',
            name='request_antecipation',
        ),
        migrations.AddField(
            model_name='logtransactions',
            name='req_antecipation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='antecipation.requestantecipation'),
        ),
    ]
