from django.contrib.auth.models import AbstractUser
from django.db import models

class CurrentNews(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

class User(AbstractUser):
    username = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    points_balance = models.IntegerField(default=0)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions', blank=True
    )  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        return self.fullname



# models.py

class HelpRequest(models.Model):
    CATEGORY_CHOICES = [
        ('medical', 'Медична допомога'),
        ('food', 'Продукти харчування'),
        ('transport', 'Транспорт'),
        ('other', 'Інше'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='help_requests')  # хто відправив
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_requests')  # хто прийняв

    title = models.CharField(max_length=200)  # назва
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)  # категорія
    description = models.TextField()  # опис
    name = models.CharField(max_length=100)  # ім’я людини, що потребує допомоги
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)  # дата і час публікації
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Очікує'), ('in_progress', 'В процесі'), ('completed', 'Завершено')],
        default='pending'
    )

    def __str__(self):
        return f"{self.title} ({self.category}) - {self.requester.fullname}"




class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    RATING_CHOICES = [
        (1, 'Погано'),
        (2, 'Середньо'),
        (3, 'Добре'),
    ]

    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
