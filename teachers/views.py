from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from education.forms import VideoUploadForm
from education.models import Lesson, Group, Attendance, Video
from teachers.models import Teacher
from .forms import LessonForm


@login_required(login_url='education:login')
def profile(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    context = {
        'teacher': teacher,
    }

    return render(request, 'teachers/profile.html', context)


@login_required(login_url='education:login')
def groups_list(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    groups = teacher.group_teacher.all()

    context = {
        'teacher': teacher,
        'groups': groups,
    }

    return render(request, 'teachers/groups.html', context)


@login_required(login_url='education:login')
def lessons_list(request, pk):
    group = get_object_or_404(Group, id=pk)
    teacher = get_object_or_404(Teacher, id=group.teacher.id)
    lessons = group.lessons.all()

    context = {
        'group': group,
        'lessons': lessons,
        'teacher': teacher,
    }

    return render(request, 'teachers/lessons.html', context)


@login_required(login_url='education:login')
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    group = get_object_or_404(Group, id=lesson.group.id)
    teacher = get_object_or_404(Teacher, id=group.teacher.id)
    students = group.groups_of_students.all()
    videos = Video.objects.filter(lesson=lesson)

    for student in students:
        student.attendance, _ = Attendance.objects.get_or_create(
            student=student.student,
            lesson=lesson
        )

    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.lesson = lesson
            video.save()
            return redirect('teachers:lesson_detail', pk=pk)
    else:
        form = VideoUploadForm()

    context = {
        'lesson': lesson,
        'teacher': teacher,
        'group': group,
        'students': students,
        'videos': videos,
        'form': form,
    }
    return render(request, 'teachers/lesson_detail.html', context)


@login_required(login_url='education:login')
def update_attendance(request, lesson_id):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("attendance_"):
                student_id = key.split("_")[1]
                is_present = value == "on"

                attendance, _ = Attendance.objects.get_or_create(
                    student_id=student_id,
                    lesson_id=lesson_id
                )
                attendance.is_present = is_present
                attendance.save()

    return redirect("teachers:lesson_detail", pk=lesson_id)


@login_required(login_url="education:login")
def add_lesson(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    teacher = get_object_or_404(Teacher, id=group.teacher.id)

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.group = group
            lesson.save()
            return redirect(reverse("teachers:lessons", kwargs={"pk": group_id}))
    else:
        form = LessonForm()

    context = {
        'group': group,
        'teacher': teacher,
        'form': form,
    }
    return render(request, "teachers/add_lesson.html", context)