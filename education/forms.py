from django import forms
from .models import Video, Homework

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['description', 'file', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }