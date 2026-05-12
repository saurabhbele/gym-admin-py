from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'members', api_views.MemberProfileViewSet, basename='member')
router.register(r'weight-logs', api_views.WeightLogViewSet, basename='weightlog')
router.register(r'exercise-logs', api_views.ExerciseLogViewSet, basename='exerciselog')
router.register(r'payments', api_views.PaymentViewSet, basename='payment')
router.register(r'exercises', api_views.ExerciseViewSet, basename='exercise')

urlpatterns = [
    path('login/', api_views.CustomAuthToken.as_view(), name='api_login'),
    path('profile/', api_views.CurrentMemberProfileView.as_view(), name='api_current_profile'),
    path('', include(router.urls)),
]
