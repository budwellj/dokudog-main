from rest_framework.viewsets import ModelViewSet
from .models import Work
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .serializers import WorkSerializer
from django.conf import settings
import requests

class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

@login_required
def get_recommendation_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        recommendation_url = f'http://127.0.0.1:8000/api/recommendation/{user_id}/'  # Adjust port if necessary

        # Use the shared service key for authentication
        headers = {'Service-Key': settings.SERVICE_SECRET_KEY}

        try:
            response = requests.get(recommendation_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            recommendation = data.get('recommendation')
            if recommendation:
                return render(request, 'dokudog/recommendation.html', {'recommendation': recommendation})
            else:
                error = 'No recommendation found.'
        except requests.exceptions.RequestException as e:
            error = f'An error occurred: {e}'

        return render(request, 'dokudog/recommendation.html', {'error': error})
    else:
        return render(request, 'dokudog/recommendation.html')