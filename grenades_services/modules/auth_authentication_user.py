


from django.contrib.auth import authenticate
from django.contrib.auth import login

class Authentication:
    """
    Authentication
    """
    def __init__(self, auth_user_instance, password=None, request=None):
        self.auth_user_instance = auth_user_instance
        self.password = password
        self.request = request

    def web_authentication(self):
        """
        This 'web_authentication' method used to create django login session
        """
        if self.password:
            _password = self.password
        else:
            _password = self.auth_user_instance.password
        _authenticate = authenticate(username=str(self.auth_user_instance.username),
                                     password=str(_password))
        if _authenticate:
            login(self.request, _authenticate)
            return True

    def api_authentication(self):
        """
        This 'api_authentication' method used to create token generation apis
        """
        pass