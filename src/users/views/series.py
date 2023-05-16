import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views import View

from users.models import Series


class SeriesDataView(View):
    async def get(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        """Get all the series and their articles."""

        series_data = []
        async for series in Series.objects.prefetch_related('articles_set').all():
            data = {
                'id': str(series.id),
                'name': series.name,
                'image': series.image.url,
                'articles': [],
            }

            async for article in series.articles_set.all():
                article_data = {
                    'id': str(article.id),
                    'title': article.title,
                    'url': article.url,
                }
                data['articles'].append(article_data)
            series_data.append(data)

        response_data = json.loads(json.dumps(series_data))

        return JsonResponse(response_data, status=200, safe=False)
