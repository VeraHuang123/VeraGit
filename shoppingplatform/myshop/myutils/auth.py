from rest_framework.authentication import BaseAuthentication
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from user.models import User

class JwtAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN',"")
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        except (jwt.DecodeError,jwt.InvalidSignatureError):
            raise AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token expired')

        email = payload['email']
        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed('Invalid token')

        return user,None