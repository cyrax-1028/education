import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailConfirmation
from teachers.models import Teacher, Student
from phonenumber_field.phonenumber import PhoneNumber

# Create your views here.

def index(request):
    return render(request, template_name='education/home.html')


# //////////////////// A U T H E N T I C A T I O N ////////////////////////
def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        role = request.POST.get("role")

        if password1 != password2:
            messages.error(request, "Parollar mos kelmadi!")
            return redirect("education:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro‘yxatdan o‘tgan!")
            return redirect("education:register")

        user = User.objects.create_user(username=email, email=email,first_name=first_name, last_name=last_name, password=password1, is_active=False)
        user.save()

        if role == "teacher":
            phone_number = request.POST["teacher_phone"]
            Teacher.objects.create(
                user=user,
                phone_number=PhoneNumber.from_string(phone_number, region="UZ"),
                address=request.POST["teacher_address"],
                job=request.POST["teacher_job"],
                bio=""
            )
        elif role == "student":
            phone_number = request.POST["student_phone"]
            Student.objects.create(
                full_name=request.POST["student_full_name"],
                phone_number=PhoneNumber.from_string(phone_number, region="UZ"),
                address=request.POST["student_address"],
                bio=""
            )

        token = str(uuid.uuid4())
        EmailConfirmation.objects.create(user=user, token=token)

        confirmation_link = request.build_absolute_uri(reverse("education:confirm_email", args=[token]))

        send_mail(
            "Email tasdiqlash",
            f"Hurmatli foydalanuvchi, iltimos, quyidagi havola orqali ro‘yxatdan o‘tishni tasdiqlang: {confirmation_link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Tasdiqlash havolasi emailingizga yuborildi!")
        return render(request, "education/Authentication/email_confirmation_sent.html")

    return render(request, "education/Authentication/register.html")

def confirm_email(request, token):
    try:
        confirmation = EmailConfirmation.objects.get(token=token)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()

        backend = 'django.contrib.auth.backends.ModelBackend'
        user.backend = backend

        login(request, user)
        messages.success(request, "Email tasdiqlandi! Xush kelibsiz!")
        return redirect("education:index")

    except EmailConfirmation.DoesNotExist:
        messages.error(request, "Noto‘g‘ri yoki eskirgan tasdiqlash havolasi!")
        return redirect("education:register")


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]  # username -> email
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            send_mail(
                "Kirish muvaffaqiyatli!",
                f"Hurmatli {user.email}, siz RapqonEdu tizimiga muvaffaqiyatli kirdingiz!",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect("education:index")
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri!")
            return redirect("education:login")

    return render(request, "education/Authentication/login.html")


def user_logout(request):
    if request.user.is_authenticated:
        send_mail(
            "Chiqish amalga oshirildi!",
            f"Hurmatli {request.user.username}, siz RapqonEdu tizimidan chiqdingiz!",
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
    logout(request)
    return redirect("education:index")