from django.contrib.auth import authenticate, login
import base64


class BasicAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'HTTP_AUTHORIZATION' in request.META:
            auth_string = request.META['HTTP_AUTHORIZATION']
            auth_string = auth_string.split(' ')[-1]
            username, password = str(base64.b64decode(auth_string)).split(':')
            username = username[2:]
            password = password[:-1]

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                response.status_code = 401

        return response
