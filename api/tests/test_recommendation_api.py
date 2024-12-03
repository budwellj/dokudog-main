# main_app/tests/test_recommendation_api.py

import pytest
from django.contrib.auth.models import User
from api.models import UserProfile, Theme
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_recommendation_api():
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpass')
    user.save()

    # Create a user profile
    profile = UserProfile.objects.create(
        user=user,
        difficulty_score=0.7,
        native_language='English',
        target_language='Japanese'
    )

    # Add themes to the profile
    theme1 = Theme.objects.create(name='Technology')
    theme2 = Theme.objects.create(name='Art')
    profile.themes.set([theme1, theme2])
    profile.save()

    # Obtain authentication token
    client = APIClient()
    response = client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    token = response.data['access']

    # Use the token to authenticate
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Call the recommendation API
    response = client.get(f'/api/recommendation/{user.id}/')
    assert response.status_code == 200
    assert 'recommendation' in response.data
