from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    list_filter = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
