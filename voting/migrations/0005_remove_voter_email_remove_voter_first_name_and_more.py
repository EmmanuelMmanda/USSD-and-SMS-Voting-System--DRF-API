# Generated by Django 4.2 on 2023-04-22 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("voting", "0004_alter_vote_unique_together_vote_position_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="voter", name="email",),
        migrations.RemoveField(model_name="voter", name="first_name",),
        migrations.RemoveField(model_name="voter", name="last_name",),
        migrations.RemoveField(model_name="voter", name="password",),
        migrations.AddField(
            model_name="voter",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="voter",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]