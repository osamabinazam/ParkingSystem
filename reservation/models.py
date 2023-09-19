from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from parking.models import ParkingSpace
from user.models import User
from django.utils import timezone 


class Reservation(models.Model):
    # Existing fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)
    # New fields for time limitation
    start_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_time = models.DateTimeField(default=timezone.now)

    # user_type = models.CharField(max_length=10, choices=[('employee', 'Employee'), ('guest', 'Guest')], default='employee')

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username}"
