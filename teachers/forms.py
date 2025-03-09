from django import forms
from education.models import Lesson
from .models import Teacher
from django.contrib.auth.models import User


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dars nomi"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class TeacherProfileEditForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['bio', 'phone_number', 'address', 'job']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']