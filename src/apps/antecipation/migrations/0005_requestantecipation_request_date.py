# Generated by Django 4.1.6 on 2023-02-21 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antecipation', '0004_rename_requester_antecipation_operator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestantecipation',
            name='request_date',
            field=models.DateField(default=''),
            preserve_default=False,
        ),
    ]
