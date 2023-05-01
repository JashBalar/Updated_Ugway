from .models import Turf, Rating, Timings, Booking, Profile
from rest_framework import serializers
from django.core.serializers.json import Serializer


class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class PartialTurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = ['id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact']


class TemporaryTurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = ['name']


class TimingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timings
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
