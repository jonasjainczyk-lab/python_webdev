from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here
# This ensures passwords remain hashed and hidden when editing users in admin
admin.site.register(User, UserAdmin)
