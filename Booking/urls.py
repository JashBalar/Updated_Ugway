from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import RegisterTurf, GetTurf, GetTurfDetails, GiveTurfRating, GetTurfRating, GiveTurfTimings, BookTurf, \
    GetBookings, OTPSend, OTPVerify, ManagerTotalTurfs, ManagerTurfDetails, ProfileDetails, GetManagerBookings, \
    ManagerBookTurf

urlpatterns = [
                  path('register-turf/', RegisterTurf.as_view()),
                  path('get-turf/', GetTurf.as_view()),
                  path('get-turf-details/', GetTurfDetails.as_view()),
                  path('give-turf-rating/', GiveTurfRating.as_view()),
                  path('get-turf-rating/', GetTurfRating.as_view()),
                  path('give-turf-timings/', GiveTurfTimings.as_view()),
                  path('book-turf/', BookTurf.as_view()),
                  path('book-manager-turf/', ManagerBookTurf.as_view()),
                  path('get-bookings/', GetBookings.as_view()),
                  path('get-manager-bookings/', GetManagerBookings.as_view()),
                  path('otp-send/', OTPSend.as_view()),
                  path('otp-verify/', OTPVerify.as_view()),
                  path('manager-total-turfs/', ManagerTotalTurfs.as_view()),
                  path('manager-turf-details/', ManagerTurfDetails.as_view()),
                  path('profile-details/', ProfileDetails.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
