from django.test import Client, TestCase
from django.urls import reverse

from django_auth.test_settings import common_settings
from tests.users.test_models import ArticlesFactory, SeriesFactory


@common_settings
class SeriesDataViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.client = Client()
        self.url = reverse('users:series_data')

    def test_get_series_data(self):
        """Test get series data."""
        series = SeriesFactory.create()
        articles = ArticlesFactory.create(series=series)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()[0]['id'], str(series.id))
        self.assertEqual(response.json()[0]['articles'][0]['id'], str(articles.id))
