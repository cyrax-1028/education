from django.urls import path
from teachers import views

app_name = 'teachers'

urlpatterns = [
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('teacher_groups/<int:pk>/', views.groups_list, name='groups'),
    path('group_lessons/<int:pk>/', views.lessons_list, name='lessons'),
    path('lesson_detail/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/update_attendance/', views.update_attendance, name='update_attendance'),
]