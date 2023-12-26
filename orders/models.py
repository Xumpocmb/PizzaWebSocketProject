from django.db import models
from django.contrib.auth.models import AbstractUser


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    items = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class User(AbstractUser):
    hint = models.CharField(max_length=255, null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('operator', 'Оператор'),
        ('chef', 'Повар'),
    ]
    role = models.CharField(max_length=50)  # Роль: "повар" или "оператор"

    def __str__(self):
        return self.user.username
