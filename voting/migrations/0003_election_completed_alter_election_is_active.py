# Generated by Django 4.0.1 on 2023-07-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_alter_election_voters'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='election',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
