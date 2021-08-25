from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'won_games', 'lost_games', 'draw_games', 'front_id')
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        ('Info', {'fields': ('first_name', 'last_name', 'email', 'password', 'image')}),
        ('History', {'fields':('won_games', 'lost_games', 'draw_games')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'first_name', 'last_name', 'won_games', 'lost_games', 'draw_games', 'image')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'won_games', 'lost_games', 'draw_games')


admin.site.register(CustomUser, CustomUserAdmin)