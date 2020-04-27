from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from account.models import Account
from account.serializers import RegistrationSerializer, ChangePasswordSerializer, AccountSerializer


@api_view(['POST',])
def registration_view(request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered a new user'
            data['email'] = account.email
            data['username'] = account.username
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        data = {}
        data['response'] = 'You successfully logged out'
        return Response(status=status.HTTP_200_OK, data=data)

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Account.objects.all()

    serializer_class = AccountSerializer