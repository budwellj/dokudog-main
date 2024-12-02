from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Work, Theme

class WorkTests(APITestCase):
    # create the test works in the API db. In this case, we are testing Dune. 
    def setUp(self):
        # Create themes
        self.theme_sci_fi = Theme.objects.create(name="Sci-Fi")
        self.theme_fantasy = Theme.objects.create(name="Fantasy")

        # Create a work with themes
        self.work = Work.objects.create(title="Dune", author="Frank Herbert", difficulty=10)
        self.work.themes.add(self.theme_sci_fi, self.theme_fantasy)

    def test_get_work_with_themes(self):
        url = reverse('work-detail', kwargs={'pk': self.work.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Dune")
        self.assertEqual(response.data['author'], "Frank Herbert")
        self.assertEqual(response.data['difficulty'], 10)

        theme_names = {theme['name'] for theme in response.data['themes']}

        self.assertEqual(
            theme_names,
            {self.theme_sci_fi.name, self.theme_fantasy.name}
        )
