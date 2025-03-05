from django import forms
from education.models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dars nomi"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }