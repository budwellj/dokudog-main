# main_app/tests/test_recommendation_service.py

from django.test import TestCase
from api.utils import get_sum_from_recommendation_service

class RecommendationServiceTests(TestCase):
    def test_add_function(self):
        x = 3
        y = 5
        result = get_sum_from_recommendation_service(x, y)
        self.assertEqual(result, 8)