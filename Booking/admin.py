from django.contrib import admin
from .models import Turf, Rating, Timings, Booking, Profile
from import_export.admin import ExportActionMixin


class TurfAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'manager', 'start_time', 'end_time', 'landmark', 'street', 'area', 'city', 'state',
                    'pincode', 'contact', 'email', 'length', 'width', 'longitude', 'latitude', 'image', 'total_nets',
                    'description', 'price', 'verified')


class RatingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('turf', 'rating_1_count', 'rating_2_count', 'rating_3_count', 'rating_4_count', 'rating_5_count')


class TimingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('turf', 'date', 'start_time', 'end_time')


class BookingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('turf', 'user', 'contact', 'email', 'date', 'time', 'duration', 'price')


admin.site.register(Turf, TurfAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Timings, TimingAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Profile)
