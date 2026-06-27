from django.contrib import admin
from .models import Service, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'duration',
    )

    search_fields = (
        'name',
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id',
        'customer_name',
        'service',
        'amount',
        'payment_status',
        'status',
        'date',
        'time',
    )

    list_filter = (
        'status',
        'payment_status',
        'service',
        'date',
    )

    search_fields = (
        'booking_id',
        'customer_name',
        'email',
        'phone',
    )

    ordering = (
        '-created_at',
    )

    list_editable = (
        'payment_status',
        'status',
    )

    list_per_page = 15