# Generated by Django 4.1.7 on 2023-09-20 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_user_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReservationHistory',
        ),
    ]