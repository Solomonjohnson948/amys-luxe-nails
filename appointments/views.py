from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm
from .models import Appointment


# ==========================
# Home Page
# ==========================
def home(request):
    return render(request, "home.html")


# ==========================
# Book Appointment
# ==========================
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            # Prevent double booking
            exists = Appointment.objects.filter(
                date=appointment.date,
                time=appointment.time
            ).exists()

            if exists:
                form.add_error(
                    None,
                    "This time slot has already been booked. Please choose another time."
                )
            else:
                appointment.save()

                return redirect(
                    "payment",
                    appointment_id=appointment.id
                )

    else:
        form = AppointmentForm()

    return render(request, "book.html", {
        "form": form
    })


# ==========================
# Payment Page
# ==========================
def payment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    if request.method == "POST":
        appointment.payment_status = "Paid"
        appointment.save()

        return redirect(
            "booking_success",
            appointment_id=appointment.id
        )

    return render(request, "payment.html", {
        "appointment": appointment
    })


# ==========================
# Booking Successful
# ==========================
def booking_success(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    return render(request, "success.html", {
        "appointment": appointment
    })


# ==========================
# Track Booking
# ==========================
def track_booking(request):
    appointment = None
    error = None

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")

        try:
            appointment = Appointment.objects.get(
                booking_id=booking_id
            )

        except Appointment.DoesNotExist:
            error = "No booking found with that Booking ID."

    return render(request, "track.html", {
        "appointment": appointment,
        "error": error
    })


# ==========================
# Admin Dashboard
# ==========================
def admin_dashboard(request):

    appointments = Appointment.objects.all().order_by("-created_at")

    total_bookings = appointments.count()
    pending = appointments.filter(status="Pending").count()
    approved = appointments.filter(status="Approved").count()
    completed = appointments.filter(status="Completed").count()
    cancelled = appointments.filter(status="Cancelled").count()
    revenue = appointments.filter(payment_status="Paid").count()

    return render(request, "admin_dashboard.html", {
        "appointments": appointments,
        "total_bookings": total_bookings,
        "pending": pending,
        "approved": approved,
        "completed": completed,
        "cancelled": cancelled,
        "revenue": revenue,
    })

def approve_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Approved"
    appointment.save()
    return redirect("admin_dashboard")


def complete_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Completed"
    appointment.save()
    return redirect("admin_dashboard")


def cancel_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Cancelled"
    appointment.save()
    return redirect("admin_dashboard")