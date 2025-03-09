from django.urls import path
from teachers import views

app_name = 'teachers'

urlpatterns = [
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('teacher_groups/<int:pk>/', views.groups_list, name='groups'),
    path('group_lessons/<int:pk>/', views.lessons_list, name='lessons'),
    path('lesson_detail/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/update_attendance/', views.update_attendance, name='update_attendance'),
    path('group/<int:group_id>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
    path('homework/create/<int:lesson_id>/', views.create_homework, name='create_homework'),
    path('homework/edit/<int:lesson_id>/', views.edit_homework, name='edit_homework'),
    path('homework/delete/<int:lesson_id>/', views.delete_homework, name='delete_homework'),
]
