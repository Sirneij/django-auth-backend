import json
from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.models import UserProfile


@method_decorator(csrf_exempt, name='dispatch')
class LoginPageView(View):
    async def post(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        data = json.loads(request.body.decode("utf-8"))
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return JsonResponse({'error': 'Please provide email and password'}, status=400)

        user = await sync_to_async(authenticate)(
            email=data['email'],
            password=data['password'],
        )

        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        await sync_to_async(login)(request, user)

        user_details = await UserProfile.objects.filter(user=user).select_related('user').aget()

        res_data = {
            'id': str(user_details.user.pk),
            'email': user_details.user.email,
            'first_name': user_details.user.first_name,
            'last_name': user_details.user.last_name,
            'is_staff': user_details.user.is_staff,
            'is_active': user_details.user.is_active,
            'date_joined': str(user_details.user.date_joined),
            'thumbnail': user_details.user.thumbnail.url() if user_details.user.thumbnail else None,
            'profile': {
                'id': str(user_details.id),
                'user_id': str(user_details.user.pk),
                'phone_number': user_details.phone_number,
                'github_link': user_details.github_link,
                'birth_date': str(user_details.birth_date) if user_details.birth_date else None,
            },
        }

        response_data = json.loads(json.dumps(res_data))

        return JsonResponse(response_data)
