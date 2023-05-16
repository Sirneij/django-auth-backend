from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Articles, Series, User, UserProfile


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
class UserProfileAdmin(admin.ModelAdmin):  # type:ignore
    list_display = ('user_email', 'phone_number', 'github_link', 'birth_date')

    @admin.display(ordering="user__email")
    def user_email(self, obj: UserProfile) -> str:
        """Return the user's email."""
        return obj.user.email  # pragma: no cover


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):  # type:ignore
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):  # type:ignore
    list_display = ('id', 'title', 'url', 'series_name')

    @admin.display(ordering="user__email")
    def series_name(self, obj: Articles) -> str:
        """Return the series's name."""
        return obj.series.name  # pragma: no cover
