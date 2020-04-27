from rest_framework import serializers

from hotel.models import Hotel, RoomCategory, Room, Booking


class HotelSerializer(serializers.ModelSerializer):


    class Meta:
        model = Hotel
        fields = ['name']


class RoomCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomCategory
        fields = ['hotel', 'name', 'min_price']


class RoomSerializer(serializers.ModelSerializer):


    class Meta:
        model = Room
        fields = ['room_category', 'name']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['room', 'date_check_in', 'date_check_out']

    def validate(self, attrs):
        return attrs

    # def save(self,):
    #     booking = Booking(room=self.validated_data['room'], date_check_in=self.validated_data['date_check_in'],
    #                       date_check_out=self.validated_data['date_check_out'])
    #     booking.save()
    #     return booking
