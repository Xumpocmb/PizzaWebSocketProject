from django.contrib import admin
from .models import Order, User, UserProfile


admin.site.register(Order)
admin.site.register(User)
admin.site.register(UserProfile)
