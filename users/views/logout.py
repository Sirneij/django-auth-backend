from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View, LoginRequiredMixin):
    async def post(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        await sync_to_async(logout)(request)
        return JsonResponse({'message': 'You have successfully logged out'}, status=200)
