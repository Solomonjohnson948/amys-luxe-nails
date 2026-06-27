from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'book/',
        views.book_appointment,
        name='book'
    ),

    path(
        'payment/<int:appointment_id>/',
        views.payment,
        name='payment'
    ),

    path(
        'success/<int:appointment_id>/',
        views.booking_success,
        name='booking_success'
    ),

    path(
        'track/',
        views.track_booking,
        name='track'
    ),

    path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard",
),

path(
    "approve/<int:appointment_id>/",
    views.approve_booking,
    name="approve_booking",
),

path(
    "complete/<int:appointment_id>/",
    views.complete_booking,
    name="complete_booking",
),

path(
    "cancel/<int:appointment_id>/",
    views.cancel_booking,
    name="cancel_booking",
),
]