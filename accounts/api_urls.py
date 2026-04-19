from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'members', api_views.MemberProfileViewSet, basename='member')
router.register(r'weight-logs', api_views.WeightLogViewSet, basename='weightlog')
router.register(r'exercise-logs', api_views.ExerciseLogViewSet, basename='exerciselog')
router.register(r'payments', api_views.PaymentViewSet, basename='payment')
router.register(r'exercises', api_views.ExerciseViewSet, basename='exercise')

urlpatterns = [
    path('get-token/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
]
