from django.shortcuts import render
from django.http import JsonResponse
from firebase_auth import firebase_login_required



def home(request):
    return render(request, 'myapp/index.html')

def about(request):
    return render(request, 'myapp/about.html')

def log_in(request):
    return render(request, 'myapp/log_in.html')

def sign_up(request):
    return render(request, 'myapp/sign_up.html')

def instruction(request):
    return render(request, 'myapp/instruction.html')

def profile(request):
    return render(request, 'myapp/profile.html')

def sign_up_two(request):
    return render(request, 'myapp/sign_up_two.html')

def vhidna_strinka(request):
    return render(request, 'myapp/vhidna_storinka.html')

def zayavki(request):
    return render(request, 'myapp/zayavki.html')

def detail_zayavki(request):
    return render(request, 'myapp/detail_zayavki.html')


@firebase_login_required
def my_secure_view(request):
    return JsonResponse({'message': 'Hello, Firebase user!', 'uid': request.firebase_user['uid']})
