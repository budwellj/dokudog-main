from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkViewSet, get_recommendation_view

router = DefaultRouter()
router.register(r'works', WorkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
