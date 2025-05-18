from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('log_in/', CustomLoginView.as_view(), name='log_in'), #views.log_in
    path('sign_up/', views.sign_up, name='sign_up'),
    path('instruction/', views.instruction, name='instruction'),
    # path('profile/', login_required(views.profile), name='profile'),  
    path('profile/', views.my_profile_redirect, name='profile'),
    path('vhidna_storinka/', views.vhidna_strinka, name='vhidna_storinka'),
    path('sign_up_two/', views.sign_up_two, name='sign_up_two'),
    path('zayavki/', views.help_requests_list, name='zayavki'),
    path('detail_zayavki/<int:pk>/', views.detail_zayavki, name='detail_zayavki'),
    path('contact_support/', views.contact_support, name='contact_support'),
    path('logout/', LogoutView.as_view(next_page='log_in'), name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    # path('requests/', views.help_requests_list, name='help_requests_list'),
    path('requests/create/', views.create_help_request, name='create_help_request'),
    path('zayavki/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('zayavki/creator-complete/<int:request_id>/', views.creator_complete_request, name='creator_complete_request'),
    path('zayavki/delete/<int:pk>/', views.delete_request, name='delete_request'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
