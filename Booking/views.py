import random
from datetime import timedelta, time, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.decorators import method_decorator
from .serializers import TurfSerializer, RatingSerializer, TimingsSerializer, BookingSerializer, PartialTurfSerializer
from .models import Turf, Rating, Timings, Booking, Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helper import MessageHandler


class RegisterTurf(APIView):
    @staticmethod
    def post(request):
        serializer = TurfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Rating.objects.create(turf_id=Turf.objects.get(id=serializer.data['id']))
            return Response({'message': 'Turf registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTurf(APIView):
    @staticmethod
    def get(request):
        turf = Turf.objects.all().values('id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact')
        serializer = PartialTurfSerializer(turf, many=True)
        ids = []
        for i in serializer.data:
            ids.append(i['id'])
        rating = Rating.objects.filter(turf_id__in=ids)
        rating_serializer = RatingSerializer(rating, many=True)
        return Response({'turf': serializer.data, 'rating': rating_serializer.data}, status=status.HTTP_200_OK)


class GetTurfDetails(APIView):
    @staticmethod
    def get(request):
        turf = Turf.objects.get(id=request.GET.get('id'))
        serializer = TurfSerializer(turf)
        start_time = turf.start_time
        end_time = turf.end_time
        time_slots = []
        while start_time <= end_time:
            time_slots.append(start_time.strftime("%H:%M"))
            start_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time().strftime("%H:%M")
            start_time = datetime.strptime(start_time, "%H:%M").time()
        available_nets = []
        for time_slot in time_slots:
            if len(Booking.objects.filter(turf_id=turf.id, date=request.GET.get('date'),
                                          time=time_slot)) < turf.total_nets:
                if Timings.objects.filter(turf_id=turf.id, start_time=time_slot, date=request.GET.get('date')).exists():
                    available_nets.append({
                        'time': time_slot, 'available': turf.total_nets - len(Booking.objects.filter(
                            turf_id=turf.id, date=request.GET.get('date'), time=time_slot)),
                        'price': Timings.objects.filter(
                            turf_id=turf.id, start_time=time_slot, date=request.GET.get('date')).values('price')
                    })
                else:
                    available_nets.append({'time': time_slot, 'available': turf.total_nets - len(Booking.objects.filter(
                        turf_id=turf.id, date=request.GET.get('date'), time=time_slot))})
        return Response({'turf': serializer.data, 'available_nets': available_nets}, status=status.HTTP_200_OK)


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


class GiveTurfTimings(APIView):
    @staticmethod
    def post(request):
        serializer = TimingsSerializer(data=request.data)
        if serializer:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class BookTurf(APIView):
    @staticmethod
    def post(request):
        """
        "details": [
        {
            "date": "",
            "time": "",
            "price": ""
        },
        {
            "date": "",
            "time": "",
            "price": ""
        }
    ]
        :param request:
        :return:
        """
        booking_data = request.data
        turf_data = booking_data['turf']
        user_data = booking_data['user']
        contact_data = booking_data['contact']
        booking_details = booking_data['details']
        serializers = []
        booked = []
        for i in booking_details:
            if len(Booking.objects.filter(turf_id=turf_data, date=booking_details[i]['date'],
                                          time=booking_details[i]['time'])) == 3:
                booked.append(booking_details[i])
                pass
            serializers.append(BookingSerializer(data={
                'turf': turf_data,
                'user': user_data,
                'contact': contact_data,
                'date': i['date'],
                'time': i['time'],
                'price': i['price']
            }))
        if booked:
            return Response({'booked': booked}, status=status.HTTP_400_BAD_REQUEST)
        for serializer in serializers:
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers, status=status.HTTP_201_CREATED)


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
