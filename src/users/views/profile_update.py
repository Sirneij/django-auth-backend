import json
from io import BytesIO
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.http.multipartparser import MultiPartParser
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.models import UserProfile


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(View, LoginRequiredMixin):
    def patch(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        """Handle user updates."""
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'You are not logged in. Kindly ensure you are logged in and try again'}, status=401
            )
        data, files = MultiPartParser(
            request.META, BytesIO(request.body), request.upload_handlers, request.encoding
        ).parse()

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        thumbnail = files.get('thumbnail')
        phone_number = data.get('phone_number')
        birth_date = data.get('birth_date')
        github_link = data.get('github_link')

        user_details = UserProfile.objects.filter(user=request.user).select_related('user').get()
        if first_name:
            user_details.user.first_name = first_name

        if last_name:
            user_details.user.last_name = last_name

        if thumbnail:
            user_details.user.thumbnail = thumbnail

        user_details.user.save(update_fields=['first_name', 'last_name', 'thumbnail'])

        if phone_number:
            user_details.phone_number = phone_number

        if birth_date:
            user_details.birth_date = birth_date

        if github_link:
            user_details.github_link = github_link

        user_details.save(update_fields=['phone_number', 'birth_date', 'github_link'])

        res_data = {
            'id': str(user_details.user.pk),
            'email': user_details.user.email,
            'first_name': user_details.user.first_name,
            'last_name': user_details.user.last_name,
            'is_staff': user_details.user.is_staff,
            'is_active': user_details.user.is_active,
            'date_joined': str(user_details.user.date_joined),
            'thumbnail': user_details.user.thumbnail.url if user_details.user.thumbnail else None,
            'profile': {
                'id': str(user_details.id),
                'user_id': str(user_details.user.pk),
                'phone_number': user_details.phone_number,
                'github_link': user_details.github_link,
                'birth_date': str(user_details.birth_date) if user_details.birth_date else None,
            },
        }

        response_data = json.loads(json.dumps(res_data))

        return JsonResponse(response_data, status=200)
