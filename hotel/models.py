from django.db import models

# Create your models here.
from django.db.models import CharField, ForeignKey, IntegerField, DateField


class Hotel(models.Model):
    name = CharField(max_length=100, blank=False, unique=True)


class RoomCategory(models.Model):
    hotel = ForeignKey(Hotel, on_delete=models.CASCADE)
    name = CharField(max_length=100, blank=False)
    min_price = IntegerField()

class Room(models.Model):
    room_category = ForeignKey(RoomCategory, on_delete=models.CASCADE)
    name = CharField(max_length=100)

class Booking(models.Model):
    room = ForeignKey(Room, on_delete=models.CASCADE)
    date_check_in = DateField(null=False, blank=False)
    date_check_out = DateField(null=False, blank=False)