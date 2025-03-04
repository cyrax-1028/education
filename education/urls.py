from django.urls import path
from education import views

app_name = 'education'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path("confirm-email/<str:token>/", views.confirm_email, name="confirm_email"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]