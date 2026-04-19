from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-member/', views.add_member, name='add_member'),
    path('member/<int:user_id>/', views.member_detail, name='member_detail'),
    path('member/<int:user_id>/edit/', views.edit_member, name='edit_member'),
    path('weight-log/<int:log_id>/edit/', views.edit_weight_log, name='edit_weight_log'),
    path('exercise-log/<int:log_id>/edit/', views.edit_exercise_log, name='edit_exercise_log'),
    path('member/<int:user_id>/add-weight-log/', views.add_weight_log, name='add_weight_log'),
    path('member/<int:user_id>/add-exercise-log/', views.add_exercise_log, name='add_exercise_log'),
    path('member/<int:user_id>/add-attendance/', views.add_attendance, name='add_attendance'),
    path('member/<int:user_id>/add-payment/', views.add_payment, name='add_payment'),
]
