from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# class CustomUser(AbstractUser):
#     is_teacher = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.username


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# class Group(BaseModel):
#     name = models.CharField(max_length=255)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_teacher': True})
#
#     def __str__(self):
#         return f"{self.name} ({self.course.title})"


# class Student(BaseModel):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username


# class Lesson(BaseModel):
#     title = models.CharField(max_length=255)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     date = models.DateField()
#
#     def __str__(self):
#         return f"{self.title} ({self.group.name})"


# class Attendance(BaseModel):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     is_present = models.BooleanField(default=False)

# def __str__(self):
#     return f"{self.student.user.username} - {self.lesson.title}: {'Bor' if self.is_present else 'Yo‘q'}"


# class Video(BaseModel):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     video_file = models.FileField(upload_to="videos/")
#
#     class Meta:
#         verbose_name = "Dars Videosi"
#         verbose_name_plural = "Dars Videolari"
#
#     def __str__(self):
#         return f"Video for {self.lesson.title}"

# class Grade(models.Model):
#     student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades")
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="grades")
#     score = models.PositiveIntegerField()
#
#     def __str__(self):
#         return f"{self.student.username} - {self.lesson.title} - {self.score}"

class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.token}"