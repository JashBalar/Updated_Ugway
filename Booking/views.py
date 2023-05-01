import random
from datetime import timedelta, datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import F
from django.utils.decorators import method_decorator
from .serializers import TurfSerializer, RatingSerializer, TimingsSerializer, BookingSerializer, PartialTurfSerializer, \
    ProfileSerializer, TemporaryTurfSerializer
from .models import Turf, Rating, Timings, Booking, Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helper import MessageHandler


@method_decorator(login_required, name='dispatch')
class RegisterTurf(APIView):
    @staticmethod
    def post(request):
        serializer = TurfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Rating.objects.create(turf_id=Turf.objects.get(name=serializer.data['name']).id)
            send_mail("New Turf Registered", str(serializer.data), settings.EMAIL_HOST_USER, ['goboxconfirmation@gmail.com'])
            return Response({'message': 'Turf registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class ManagerTotalTurfs(APIView):
    @staticmethod
    def get(request):
        serializer = TurfSerializer(Turf.objects.filter(manager=request.GET.get('user')), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class ManagerTurfDetails(APIView):
    @staticmethod
    def get(request):
        turf = Turf.objects.get(id=request.GET.get('id'), manager=request.GET.get('user'))
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


class GetTurf(APIView):
    @staticmethod
    def get(request):
        """
        provide filter_data and filter
        filter = 1 -> filter by name
        filter = 2 -> filter by ascending price
        filter = 3 -> filter by descending price
        filter = 4 -> filter by rating
        :param request:
        :return:
        """
        if request.GET.get('filter') == 1:
            turfs = Turf.objects.filter(name=request.GET.get('filter_data')).values(
                'id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact'
            )
        elif request.GET.get('filter') == 2:
            turfs = Turf.objects.all().order_by('price').values(
                'id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact'
            )
        elif request.GET.get('filter') == 3:
            turfs = Turf.objects.all().order_by('-price').values(
                'id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact'
            )
        elif request.GET.get('filter') == 4:
            turfs = Turf.objects.all().order_by('-rating__rating_5_count').values(
                'id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact'
            )
        else:
            turfs = Turf.objects.all().values('id', 'name', 'start_time', 'end_time', 'total_nets', 'image', 'contact')
        temp_turfs = []
        for x in turfs:
            temp_turfs.append(x)
        turfs_list = []
        for turf in temp_turfs:
            start_time = turf['start_time']
            end_time = turf['end_time']
            time_slots = []
            while start_time <= end_time:
                time_slots.append(start_time.strftime("%H:%M"))
                start_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time().strftime("%H:%M")
                start_time = datetime.strptime(start_time, "%H:%M").time()
            available_nets = []
            for time_slot in time_slots:
                if len(Booking.objects.filter(turf_id=turf['id'], date=request.GET.get('date'),
                                              time=time_slot)) < turf['total_nets']:
                    if Timings.objects.filter(turf_id=turf['id'], start_time=time_slot, date=request.GET.get('date')).exists():
                        available_nets.append({
                            'time': time_slot, 'available': turf['total_nets'] - len(Booking.objects.filter(
                                turf_id=turf['id'], date=request.GET.get('date'), time=time_slot)),
                            'price': Timings.objects.filter(
                                turf_id=turf['id'], start_time=time_slot, date=request.GET.get('date')).values('price')
                        })
                    else:
                        available_nets.append({'time': time_slot, 'available': turf['total_nets'] - len(Booking.objects.filter(
                            turf_id=turf['id'], date=request.GET.get('date'), time=time_slot))})
            rating = Rating.objects.filter(turf_id=turf['id'])
            rating_serializer = RatingSerializer(rating, many=True)
            turfs_list.append({'turf': turf, 'rating': rating_serializer.data, 'available_nets': available_nets})
        return Response({'turfs': turfs_list}, status=status.HTTP_200_OK)


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
    def put(request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating_data = request.data.get('rating')
            if rating_data == 1:
                Rating.objects.filter(turf_id=request.data.get('turf')).update(rating_1_count=F('rating_1_count') + 1)
            elif rating_data == 2:
                Rating.objects.filter(turf_id=request.data.get('turf')).update(rating_2_count=F('rating_2_count') + 1)
            elif rating_data == 3:
                Rating.objects.filter(turf_id=request.data.get('turf')).update(rating_3_count=F('rating_3_count') + 1)
            elif rating_data == 4:
                Rating.objects.filter(turf_id=request.data.get('turf')).update(rating_4_count=F('rating_4_count') + 1)
            elif rating_data == 5:
                Rating.objects.filter(turf_id=request.data.get('turf')).update(rating_5_count=F('rating_5_count') + 1)
            return Response({'message': 'Rating given successfully'}, status=status.HTTP_200_OK)


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
        if serializer.is_valid():
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
            if len(Booking.objects.filter(turf_id=turf_data, date=i['date'],
                                          time=i['time'])) == Turf.objects.get(
                    id=turf_data).total_nets:
                booked.append(i)
                pass
            serializers.append({
                'turf': turf_data,
                'user': user_data,
                'contact': contact_data,
                'date': i['date'],
                'time': i['time'],
                'price': i['price']
            })
        if booked:
            return Response({'booked': booked}, status=status.HTTP_400_BAD_REQUEST)
        for serializer in serializers:
            serial = BookingSerializer(data=serializer)
            if serial.is_valid():
                serial.save()
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers, status=status.HTTP_201_CREATED)


class GetBookings(APIView):
    @staticmethod
    def get(request):
        booking = Booking.objects.filter(user_id=request.GET.get('id'))
        serializer = BookingSerializer(booking, many=True)
        data = serializer.data
        for i in data:
            turfs = Turf.objects.filter(id=i['turf']).values('name')
            turf_serializer = TemporaryTurfSerializer(turfs, many=True)
            i.update({"name": turf_serializer.data[0]['name']})
        return Response(data, status=status.HTTP_201_CREATED)


class OTPSend(APIView):
    @staticmethod
    def post(request):
        otp = random.randint(100000, 999999)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(otp=f'{otp}')
            MessageHandler(request.data['phone_number'], otp).send_otp_via_message()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerify(APIView):
    @staticmethod
    def put(request):
        user = Profile.objects.get(phone_number=request.data['phone_number'], user=request.data['user'])
        if user.otp == request.data['otp']:
            Profile.objects.filter(phone_number=request.data['phone_number']).update(is_verified=True)
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'OTP verification failed'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetails(APIView):
    @staticmethod
    def get(request):
        profile = Profile.objects.get(user=request.GET.get('id'))
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        profile = Profile.objects.get(user=request.data['user'])
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
