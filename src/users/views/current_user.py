import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views import View

from users.models import UserProfile


class CurrentUserView(View, LoginRequiredMixin):
    def get(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        """Get current user via session."""
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    'error': 'You are not logged in. Kindly ensure you are logged in and try again'
                },
                status=401,
            )

        user_details = (
            UserProfile.objects.filter(user=request.user).select_related('user').get()
        )

        res_data = {
            'id': str(user_details.user.pk),
            'email': user_details.user.email,
            'first_name': user_details.user.first_name,
            'last_name': user_details.user.last_name,
            'is_staff': user_details.user.is_staff,
            'is_active': user_details.user.is_active,
            'date_joined': str(user_details.user.date_joined),
            'thumbnail': user_details.user.thumbnail.url
            if user_details.user.thumbnail
            else None,
            'profile': {
                'id': str(user_details.id),
                'user_id': str(user_details.user.pk),
                'phone_number': user_details.phone_number,
                'github_link': user_details.github_link,
                'birth_date': str(user_details.birth_date)
                if user_details.birth_date
                else None,
            },
        }

        response_data = json.loads(json.dumps(res_data))

        return JsonResponse(response_data, status=200)
