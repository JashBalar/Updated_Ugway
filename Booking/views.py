import random
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.decorators import method_decorator
from .serializers import TurfSerializer, RatingSerializer, TimingsSerializer, BookingSerializer
from .models import Turf, Rating, Timings, Booking, Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helper import MessageHandler


class RegisterTurf(APIView):
    @staticmethod
    def post(request):
        form_data = {
            'name': request.data['name'], 'manager': request.data['manager'], 'start_time': request.data['start_time'],
            'end_time': request.data['end_time'], 'landmark': request.data['landmark'],
            'street': request.data['street'], 'area': request.data['area'], 'city': request.data['city'],
            'state': request.data['state'], 'pincode': request.data['pincode'], 'contact': request.data['contact'],
            'email': request.data['email'], 'length': request.data['length'], 'width': request.data['width'],
            'longitude': request.data['longitude'], 'latitude': request.data['latitude'],
            'total_nets': request.data['total_nets'], 'description': request.data['description'],
            'price': request.data['price'], 'verified': request.data['verified'], 'booked': request.data['booked']
        }
        success = True
        response = []
        for images in request.FILES.getlist('image'):
            form_data['image'] = images
            serializer = TurfSerializer(data=form_data)
            if serializer.is_valid():
                serializer.save()
                response.append(serializer.data)
            else:
                success = False
        if success:
            return Response(response, status=status.HTTP_201_CREATED)
        serializer = TurfSerializer(data=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTurf(APIView):
    @staticmethod
    def get(request):
        turf = Turf.objects.all().values_list('id', 'name', 'start_time', 'end_time', 'latitude', 'longitude',
                                              'total_nets', 'image', 'contact', 'rating')
        serializer = TurfSerializer(turf, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTurfDetails(APIView):
    @staticmethod
    def get(request):
        turf = Turf.objects.get(id=request.GET.get('id'))
        serializer = TurfSerializer(turf)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GiveTurfRating(APIView):
    @staticmethod
    def post(request):
        rating_data = request.data.get('rating')
        if rating_data == 1:
            Rating.objects.filter(turf_id=request.data.get('turf_id')).update(rating_1_count=F('rating_1_count') + 1)
            rating = Rating.objects.get(turf_id=request.data.get('turf_id'))
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif rating_data == 2:
            Rating.objects.filter(turf_id=request.data.get('turf_id')).update(rating_2_count=F('rating_2_count') + 1)
            rating = Rating.objects.get(turf_id=request.data.get('turf_id'))
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif rating_data == 3:
            Rating.objects.filter(turf_id=request.data.get('turf_id')).update(rating_3_count=F('rating_3_count') + 1)
            rating = Rating.objects.get(turf_id=request.data.get('turf_id'))
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif rating_data == 4:
            Rating.objects.filter(turf_id=request.data.get('turf_id')).update(rating_4_count=F('rating_4_count') + 1)
            rating = Rating.objects.get(turf_id=request.data.get('turf_id'))
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif rating_data == 5:
            Rating.objects.filter(turf_id=request.data.get('turf_id')).update(rating_5_count=F('rating_5_count') + 1)
            rating = Rating.objects.get(turf_id=request.data.get('turf_id'))
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        rating = Rating.objects.get(turf_id=request.data.get('turf_id'))
        serializer = RatingSerializer(rating)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTurfRating(APIView):
    @staticmethod
    def get(request):
        rating = Rating.objects.get(turf_id=request.GET.get('id'))
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTurfTimings(APIView):
    @staticmethod
    def get(request):
        timings = Timings.objects.filter(turf_id=request.GET.get('id'))
        serializer = TimingsSerializer(timings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class BookTurf(APIView):
    @staticmethod
    def post(request):
        serializer = BookingSerializer(data=request.data)
        turf_id = request.data.get('turf_id')
        turf = Turf.objects.get(id=turf_id)
        if turf.booked:
            return Response({'error': 'Turf is already booked'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBookings(APIView):
    @staticmethod
    def get(request):
        booking = Booking.objects.filter(user_id=request.GET.get('id'))
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBookingDetails(APIView):
    @staticmethod
    def get(request, pk):
        booking = Booking.objects.filter(pk=pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OTPSend(APIView):
    @staticmethod
    def post(request):
        otp = random.randint(100000, 999999)
        Profile.objects.create(phone_number=request.POST.get('phone_number'), otp=f'{otp}')
        MessageHandler(request.data['phone_number'], otp).send_otp_via_message()
        return Response({}, status=status.HTTP_200_OK)


class OTPVerify(APIView):
    @staticmethod
    def post(request):
        phone_number = request.data['phone_number']
        otp = request.data['otp']
        profile = Profile.objects.get(phone_number=phone_number)
        if profile.otp == otp:
            profile.is_verified = True
            return Response({'profile': profile}, status=status.HTTP_200_OK)
        return Response({'profile': profile}, status=status.HTTP_400_BAD_REQUEST)
