# Generated by Django 4.1.7 on 2023-02-21 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ship", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="operator",
            name="pub_date",
        ),
    ]