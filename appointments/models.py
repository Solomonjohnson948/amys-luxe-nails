from django.db import models
import uuid


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='Unpaid'
    )

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # Generate booking ID once
        if not self.booking_id:
            self.booking_id = "ALN-" + uuid.uuid4().hex[:8].upper()

        # Automatically copy service price
        if self.service:
            self.amount = self.service.price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.customer_name}"