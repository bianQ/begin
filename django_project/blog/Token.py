from itsdangerous import URLSafeTimedSerializer as uts
import base64
from django.conf import settings as django_settings

class Token:
    def __init__(self, security_key):
        self.serializer = uts(security_key)
        self.salt = base64.encodebytes(security_key.encode())

    #生成token
    def generate_validate_token(self, username):
        return self.serializer.dumps(username, self.salt)

    #验证token是否过期，没有则返回token内的username
    def confirm_validate_token(self, token):
        return self.serializer.loads(token, salt=self.salt, max_age=3600)

    #无论token是否有效，提取token中的username
    def remove_validate_token(self, token):
        return self.serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY)