from django.urls import path, include
from account.views import registration_view, Logout, ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from hotel.views import HotelViewSet, RoomCategoryViewSet, RoomViewSet, BookingViewSet

app_name = 'hotel'

user_list = HotelViewSet.as_view({'get': 'list'})
room_category_list = RoomCategoryViewSet.as_view({'get': 'list'})
room_list = RoomViewSet.as_view({'get': 'list'})
router = routers.DefaultRouter()

router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'hotels', HotelViewSet, basename='hotels')
router.register(r'room_categories', RoomCategoryViewSet, basename='room_categories')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    # path('hotels', user_list),
    # path('room_categories', room_category_list),
    # path('rooms', room_list),
    path('', include(router.urls)),



]
