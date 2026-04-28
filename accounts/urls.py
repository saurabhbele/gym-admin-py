from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('member/<int:user_id>/reset-password/', views.admin_reset_password, name='admin_reset_password'),

    path('', views.dashboard, name='dashboard'),
    path('add-member/', views.add_member, name='add_member'),
    path('import-members/', views.import_members, name='import_members'),
    path('member/<int:user_id>/', views.member_detail, name='member_detail'),
    path('member/<int:user_id>/edit/', views.edit_member, name='edit_member'),
    path('weight-log/<int:log_id>/edit/', views.edit_weight_log, name='edit_weight_log'),
    path('exercise-log/<int:log_id>/edit/', views.edit_exercise_log, name='edit_exercise_log'),
    path('member/<int:user_id>/add-weight-log/', views.add_weight_log, name='add_weight_log'),
    path('member/<int:user_id>/add-exercise-log/', views.add_exercise_log, name='add_exercise_log'),
    path('member/<int:user_id>/add-attendance/', views.add_attendance, name='add_attendance'),
    path('member/<int:user_id>/add-payment/', views.add_payment, name='add_payment'),
    path('member/<int:user_id>/add-diet-plan/', views.add_diet_plan, name='add_diet_plan'),
    path('member/<int:user_id>/generate-pdf/', views.generate_member_pdf, name='generate_member_pdf'),
]
