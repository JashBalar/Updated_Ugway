from django.urls import path
from .views import RegisterTurf, GetTurf, GetTurfDetails, GiveTurfRating, GetTurfRating, GetTurfTimings, BookTurf, \
    GetBookings, GetBookingDetails, OTPSend, OTPVerify

urlpatterns = [
    path('register-turf/', RegisterTurf.as_view()),
    path('get-turf/', GetTurf.as_view()),
    path('get-turf-details/', GetTurfDetails.as_view()),
    path('give-turf-rating/', GiveTurfRating.as_view()),
    path('get-turf-rating/', GetTurfRating.as_view()),
    path('get-turf-timings/', GetTurfTimings.as_view()),
    path('book-turf/', BookTurf.as_view()),
    path('get-bookings/', GetBookings.as_view()),
    path('get-booking-details/<int:pk>/', GetBookingDetails.as_view()),
    path('otp-send/', OTPSend.as_view()),
    path('otp-verify/<int:pk>/', OTPVerify.as_view()),
]
