from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from teachers.models import Teacher, Student

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


class Group(BaseModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='group_teacher')

    def __str__(self):
        return f"{self.name} ({self.course.title})"


class Lesson(BaseModel):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.group.name})"


class Attendance(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances_student')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances_lesson')
    is_present = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_present:
            self.grade = 4
        else:
            self.grade = 0
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.lesson.title}: {'Bor' if self.is_present else 'Yo‘q'}"


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to="videos/")

    class Meta:
        verbose_name = "Dars Videosi"
        verbose_name_plural = "Dars Videolari"

    def __str__(self):
        return f"Video for {self.lesson.title}"


class Students_of_group(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="students_of_group")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="groups_of_students")

    def __str__(self):
        return f"{self.student.full_name} - {self.group.name}"

class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.token}"