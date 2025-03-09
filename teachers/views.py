from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from education.forms import VideoUploadForm, HomeworkForm
from education.models import Lesson, Group, Attendance, Video, Students_of_group, Homework
from teachers.models import Teacher
from .forms import LessonForm, TeacherProfileEditForm, UserEditForm


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
    homework = Homework.objects.filter(lesson=lesson).first()

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
        'homework': homework,
    }
    return render(request, 'teachers/lesson_detail.html', context)


@login_required(login_url='education:login')
def update_attendance(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    students = Students_of_group.objects.filter(group=lesson.group)

    if request.method == "POST":
        for student in students:
            key = f"attendance_{student.student.id}"
            is_present = request.POST.get(key) == "on"
            attendance, _ = Attendance.objects.get_or_create(student=student.student, lesson=lesson)
            attendance.is_present = is_present
            attendance.save()

        return redirect('teachers:lesson_detail', pk=lesson.id)

    return render(request, 'teachers/lesson_detail.html', {'lesson': lesson, 'students': students})


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


@login_required(login_url="education:login")
def edit_profile(request):
    user = request.user
    teacher = user.teacher_profile

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        teacher_form = TeacherProfileEditForm(request.POST, instance=teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            return redirect('teachers:profile', pk=teacher.id)
    else:
        user_form = UserEditForm(instance=user)
        teacher_form = TeacherProfileEditForm(instance=teacher)

    return render(request, 'teachers/edit_profile.html', {'user_form': user_form, 'teacher_form': teacher_form})


@login_required(login_url="education:login")
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return redirect('teachers:lesson_detail', pk=video.lesson.id)


@login_required(login_url="education:login")
def create_homework(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    if request.method == "POST":
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.lesson = lesson
            homework.save()
            return redirect('teachers:lesson_detail', lesson_id=lesson.id)

    else:
        form = HomeworkForm()

    return render(request, 'teachers/homework_create.html', {'form': form, 'lesson': lesson})


@login_required(login_url="education:login")
def edit_homework(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    homework = get_object_or_404(Homework, lesson=lesson)

    if request.method == "POST":
        form = HomeworkForm(request.POST, request.FILES, instance=homework)
        if form.is_valid():
            form.save()
            return redirect('teachers:lesson_detail', pk=lesson.id)
    else:
        form = HomeworkForm(instance=homework)

    return render(request, 'teachers/homework_edit.html', {'form': form, 'lesson': lesson})


@login_required(login_url="education:login")
def delete_homework(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    homework = get_object_or_404(Homework, lesson=lesson)

    if request.method == "POST":
        homework.delete()
        return redirect('teachers:lesson_detail', pk=lesson.id)

    return redirect('teachers:edit_homework', lesson_id=lesson.id)
