# Generated by Django 4.0.1 on 2023-07-11 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_election_completed_alter_election_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voter',
            name='date_of_birth',
        ),
    ]
