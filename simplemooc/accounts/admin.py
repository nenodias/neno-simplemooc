from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','name','is_active','is_staff','date_joined',]
    search_fields = ['username','email','name']

admin.site.register(User, UserAdmin)