from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    bio = models.TextField(max_length=500, blank=True)
    phone_number = PhoneNumberField(region="UZ")
    address = models.CharField(max_length=255, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Student(BaseModel):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = PhoneNumberField(region="UZ")
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name