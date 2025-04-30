# firebase_auth.py
from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError
from django.http import JsonResponse

def firebase_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        id_token = request.META.get('HTTP_AUTHORIZATION')
        if not id_token:
            return JsonResponse({'error': 'Token not provided'}, status=401)
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.firebase_user = decoded_token
        except InvalidIdTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
