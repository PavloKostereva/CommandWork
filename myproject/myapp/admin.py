from django.contrib import admin
from .models import HelpRequest
from .models import User
from .models import CurrentNews
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin 

admin.site.register(CurrentNews)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'fullname', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('fullname', 'phone', 'avatar', 'about', 'points_balance')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']  # обидва поля є в моделі

    # Замість неіснуючих полів використовуємо ті, що точно існують
    list_display = ['title', 'category', 'requester', 'status', 'updated_at']
    list_filter = ['status', 'category']  # category — дозволений тип для фільтра

    search_fields = ['title', 'description', 'name', 'email', 'phone']


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Особиста інформація', {'fields': ('fullname', 'email', 'about')}),
#         ('Права доступу', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Інша інформація', {'fields': ('email_verified', 'phone_verified', 'points_balance')}),
#         ('Важливі дати', {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'fullname', 'email', 'about', 'password1', 'password2'),
#         }),
#     )

#     list_display = ('username', 'fullname', 'email', 'is_staff', 'email_verified', 'phone_verified')
#     search_fields = ('username', 'fullname', 'email')
#     ordering = ('username',)

