from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.hashers import check_password
from accounts.models import Profile

class EmailOrUsernameModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Try to fetch the user by email
            user = Profile.objects.get(email=username)
        except Profile.DoesNotExist:
            # Try to fetch the user by username if email lookup fails
            try:
                user = Profile.objects.get(username=username)
            except Profile.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
