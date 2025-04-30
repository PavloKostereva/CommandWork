from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('log_in/', views.log_in, name='log_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('instruction/', views.instruction, name='instruction'),
    path('profile/', views.profile, name='profile'),
    path('vhidna_storinka/', views.profile, name='vhidna_storinka'),
    path('sign_up_two/', views.sign_up_two, name='sign_up_two'),
    path('zayavki/', views.zayavki, name='zayavki'),
    path('detail_zayavki/', views.detail_zayavki, name='detail_zayavki'),
]
