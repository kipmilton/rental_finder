from django.db import models
from django.contrib.auth.models import User

# class Rental(models.Model):
#     HOUSE_TYPES = [
#         ('Bedsitter', 'Bedsitter'),
#         ('Single Room', 'Single Room'),
#         ('One Bedroom', 'One Bedroom'),
#         ('Two Bedroom', 'Two Bedroom'),
#         ('Three Bedroom', 'Three Bedroom'),
#         ('four Bedroom', 'four Bedroom'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Associate with user
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     house_type = models.CharField(max_length=20, choices=HOUSE_TYPES)
#     location = models.CharField(max_length=255)
#     apartment_name = models.CharField(max_length=255)
#     monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.apartment_name}"


class Rental(models.Model):
    HOUSE_TYPES = [
        ('Bedsitter', 'Bedsitter'),
        ('Single Room', 'Single Room'),
        ('One Bedroom', 'One Bedroom'),
        ('Two Bedroom', 'Two Bedroom'),
        ('Three Bedroom', 'Three Bedroom'),
        ('Four Bedroom', 'Four Bedroom'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    house_type = models.CharField(max_length=20, choices=HOUSE_TYPES)
    location = models.CharField(max_length=255)
    apartment_name = models.CharField(max_length=255)
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # New status field

    def __str__(self):
        return f"{self.name} - {self.apartment_name} - {self.status}"
