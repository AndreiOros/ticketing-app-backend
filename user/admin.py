from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Organisation

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'date_joined']  # Example fields to filter by
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class OrganisationAdmin(admin.ModelAdmin):
    model = Organisation
    list_display = ['name', 'owner']
    filter_horizontal = ['members']

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
