# Generated by Django 4.1.6 on 2023-02-21 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antecipation', '0003_logtransactions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='antecipation',
            old_name='requester',
            new_name='operator',
        ),
        migrations.RenameField(
            model_name='antecipation',
            old_name='payment',
            new_name='request_antecipation',
        ),
    ]