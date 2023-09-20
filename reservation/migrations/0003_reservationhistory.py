# Generated by Django 4.1.7 on 2023-09-20 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_rename_availability_parkingspace_is_available_and_more'),
        ('reservation', '0002_reservation_end_time_reservation_start_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('booked', 'Booked'), ('canceled', 'Canceled')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('parking_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.parkingspace')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.reservation')),
            ],
        ),
    ]