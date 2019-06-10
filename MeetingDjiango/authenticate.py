from django.contrib.auth.backends import ModelBackend
from Meeting.models import Users


class DefBackend(ModelBackend):
    # 复写authenticate
    def authenticate(self, request, username=None, password=None, **kwargs):
        name = Users.objects.get(name=username)
        try:
            user = Users.objects.get(email=username)
        except:
            try:
                user = Users.objects.get(phone=username)
            except:
                return None
        # 做密码验证
        if user.check_password(password):
            return user, name
        else:
            return None
