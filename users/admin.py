from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, UserProfile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'email',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'thumbnail')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (
            None,
            {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'thumbnail', 'is_staff', 'is_active')},
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'phone_number', 'github_link', 'birth_date')

    @admin.display(ordering="user__email")
    def user_email(self, obj: UserProfile) -> str:
        return obj.user.email
