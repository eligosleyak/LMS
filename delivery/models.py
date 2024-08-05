from django.db import models
from users.models import User

class Delivery(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE)
    package_name = models.CharField(max_length=100)
    pickup_address = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    recipient_address = models.CharField(max_length=255)
    rider = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'rider', null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add = True)
    has_rider = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = True)