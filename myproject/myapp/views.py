from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, EmailLoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import HelpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError 
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
import logging
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django import forms
from .models import CurrentNews
from .models import HelpRequest
from .forms import HelpRequestForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

def home(request):
    news = CurrentNews.objects.order_by('-date')
    return render(request, 'myapp/index.html', {'news': news})

def about(request):
    return render(request, 'myapp/about.html')

class CustomLoginView(LoginView):
    authentication_form = EmailLoginForm
    template_name = 'myapp/log_in.html'

# def log_in(request):  
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('profile')
#         else:
#             messages.error(request, 'Невірний логін або пароль')
#     return render(request, 'myapp/log_in.html')

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна! Увійдіть до свого профілю.')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'myapp/sign_up.html', {'form': form})


# @login_required
# def profile(request):
#     if request.method == 'POST' and request.FILES.get('avatar'):
#         request.user.avatar = request.FILES['avatar']
#         request.user.save()
#         return redirect('profile')
#     return render(request, 'myapp/profile.html', {'user': request.user})

User = get_user_model()
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'fullname', 'phone', 'about', 'avatar']

@login_required
@require_http_methods(["GET", "POST"])
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            form_html = render_to_string('myapp/partials/edit_profile_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = ProfileUpdateForm(instance=user)
        html = render_to_string('myapp/partials/edit_profile_form.html', {'form': form}, request=request)
        return HttpResponse(html)



User = get_user_model()

def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = request.user.is_authenticated and request.user == profile_user
    applications = profile_user.help_requests.exclude(status='completed')
    accepted_requests = profile_user.accepted_requests.all()
    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'applications': applications,
        'accepted_requests': accepted_requests,
    }
    return render(request, 'myapp/profile.html', context)

@login_required
def my_profile_redirect(request):
    return redirect('user_profile', username=request.user.username)

# def profile(request):
#     return render(request, 'myapp/profile.html')

def instruction(request):
    return render(request, 'myapp/instruction.html')

def sign_up_two(request):
    return render(request, 'myapp/sign_up_two.html')

def vhidna_strinka(request):
    return render(request, 'myapp/vhidna_storinka.html')

# def zayavki(request):
#     return render(request, 'myapp/zayavki.html')

def detail_zayavki(request, pk):
    requests = get_object_or_404(HelpRequest, pk=pk)
    return render(request, 'myapp/detail_zayavki.html', {'requests': requests})


logger = logging.getLogger(__name__)

def contact_support(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            message = request.POST.get("message", "").strip()

            # Валідація даних
            if not name or not email or not message:
                return JsonResponse({"success": False, "error": "Будь ласка, заповніть всі обов'язкові поля."})
            
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({"success": False, "error": "Будь ласка, введіть коректну email адресу"})

            # Відправка email адміну
            admin_subject = f"Нове повідомлення від {name} (Техпідтримка)"
            admin_message = (
                f"Ім'я: {name}\n"
                f"Email: {email}\n"
                f"Телефон: {phone if phone else 'Не вказано'}\n\n"
                f"Повідомлення:\n{message}"
            )
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=email,
                recipient_list=["logikasun@gmail.com"],  # Ваша пошта
                fail_silently=False,
            )

            # Відправка підтвердження користувачу
            user_subject = "Ваше повідомлення прийнято (KindHelp)"
            user_message = (
                f"Дякуємо за ваше повідомлення, {name}!\n\n"
                f"Ми отримали ваш запит:\n\"{message}\"\n\n"
                f"Наша команда зв'яжеться з вами найближчим часом."
            )
            
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email="noreply@kindhelp.org",
                recipient_list=[email],
                fail_silently=False,
            )

            logger.info(f"Успішно відправлено повідомлення від {name} ({email})")
            return JsonResponse({"success": True})
            
        except Exception as e:
            logger.error(f"Помилка відправки email: {str(e)}", exc_info=True)
            return JsonResponse({"success": False, "error": f"Помилка при надсиланні: {str(e)}"})
    
    return JsonResponse({"success": False, "error": "Невірний метод запиту"})


@login_required
def help_requests_list(request):
    requests = HelpRequest.objects.filter(status='pending')

    # Пошук по address
    search_query = request.GET.get('search', '')
    if search_query:
        requests = requests.filter(address__icontains=search_query)

    # Фільтр по категорії
    category = request.GET.get('category', '')
    if category and category != 'all':
        requests = requests.filter(category=category)

    # Сортування
    sort = request.GET.get('sort', '')
    if sort == 'date_asc':
        requests = requests.order_by('created_at')
    elif sort == 'date_desc':
        requests = requests.order_by('-created_at')
    elif sort == 'alpha_asc':
        requests = requests.order_by('title')
    elif sort == 'alpha_desc':
        requests = requests.order_by('-title')
    else:
        requests = requests.order_by('-created_at')  # за замовчуванням

    form = HelpRequestForm()
    return render(request, 'myapp/zayavki.html', {
        'requests': requests,
        'form': form,
        'search_query': search_query,
        'selected_category': category,
        'selected_sort': sort,
    })

@login_required
def create_help_request(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help_request = form.save(commit=False)
            help_request.requester = request.user
            help_request.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def accept_request(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)

    # якщо заявка ще ніким не прийнята
    if help_request.accepted_by is None:
        help_request.accepted_by = request.user
        help_request.status = 'in_progress'
        help_request.save()

    return redirect('zayavki')  

@login_required
def creator_complete_request(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)

    # Перевірка: заявка прийнята і поточний користувач — той, хто її створив
    if help_request.status == 'in_progress' and help_request.requester == request.user:
        help_request.status = 'completed'
        help_request.save()

    return redirect('user_profile', username=request.user.username)

@login_required
def delete_request(request, pk):
    help_request = get_object_or_404(HelpRequest, pk=pk)

    if request.user == help_request.requester:
        help_request.delete()
    return redirect('user_profile', username=request.user.username)