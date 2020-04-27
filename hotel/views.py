from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from account.models import Account
from account.serializers import RegistrationSerializer, ChangePasswordSerializer

# Create your views here.
from hotel.models import Hotel, RoomCategory, Room, Booking
from hotel.serializers import HotelSerializer, RoomCategorySerializer, RoomSerializer, BookingSerializer


class HotelViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):
        queryset = Hotel.objects.all()
        serializer = HotelSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk):
        if pk == request.user.hotel.pk:
            hotel = Hotel.objects.get(pk=pk)
            serializer = HotelSerializer(hotel)
            return Response(serializer.data)
        else:
            return Response('You are from another hotel',status=403)


class RoomCategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = RoomCategory.objects.filter(hotel=request.user.hotel)
        serializer = RoomCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        room_category = get_object_or_404(klass=RoomCategory, pk=pk, hotel__pk=request.user.hotel.pk)
        serializer = RoomCategorySerializer(room_category)
        return Response(serializer.data)


class RoomViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Room.objects.filter(room_category__hotel=request.user.hotel)

        room_category = self.request.query_params.get('room_category', None)
        if room_category is not None:
            queryset = queryset.filter(room_category=room_category)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        room = get_object_or_404(klass=Room, pk=pk, room_category__hotel__pk=request.user.hotel.pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)


class BookingViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Booking.objects.filter(room__room_category__hotel=request.user.hotel)

        room = self.request.query_params.get('room', None)
        if room is not None:
            queryset = queryset.filter(room=room)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            if Booking.objects.filter(room__room_category__hotel=request.user.hotel).exists():
                if Booking.objects.filter(room=request.data['room'],
                                          date_check_out__gte=request.data['date_check_in'],
                                          date_check_out__lte=request.data[
                                              'date_check_out']).exists() or Booking.objects.filter(
                    room=request.data['room'],
                    date_check_in__gte=request.data['date_check_in'],
                    date_check_in__lte=request.data['date_check_out']).exists():
                    return Response("There is overlapping")
                booking = serializer.save()
                return Response(serializer.data)
            else:
                return Response("This is not your hotel, you can't book this room", status=403)
        return Response(serializer.errors)

    def retrieve(self, request, pk):
        booking = get_object_or_404(klass=Booking, pk=pk, room__room_category__hotel__pk=request.user.hotel.pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
