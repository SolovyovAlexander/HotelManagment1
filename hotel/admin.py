from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from hotel.models import Hotel, RoomCategory, Room, Booking


class HotelAdmin(UserAdmin):
    list_display = ('name' ,)
    search_fields = ('name',)
    readonly_fields = ()
    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Hotel, HotelAdmin)

class RoomCategoryAdmin(UserAdmin):
    list_display = ('hotel', 'name', 'min_price', )
    search_fields = ( 'name', 'min_price',)
    readonly_fields = ()
    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(RoomCategory, RoomCategoryAdmin)


class RoomAdmin(UserAdmin):
    list_display = ('room_category', 'name',  )
    search_fields = ( 'name', )
    readonly_fields = ()
    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Room, RoomAdmin)

class BookingAdmin(UserAdmin):
    list_display = ('room', 'date_check_in', 'date_check_out', )
    search_fields = ( 'date_check_in', 'date_check_out', )
    readonly_fields = ()
    ordering = ('date_check_in',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Booking, BookingAdmin)