import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from typing import Optional
from .models import EmailConfirmation

# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, template_name='education/home.html')


# //////////////////// A U T H E N T I C A T I O N ////////////////////////
def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Parollar mos kelmadi!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro‘yxatdan o‘tgan!")
            return redirect("register")

        user = User.objects.create_user(username=email, email=email, password=password1, is_active=False)
        user.save()

        token = str(uuid.uuid4())
        EmailConfirmation.objects.create(user=user, token=token)

        confirmation_link = request.build_absolute_uri(reverse("confirm_email", args=[token]))

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
        return redirect("product_list")

    except EmailConfirmation.DoesNotExist:
        messages.error(request, "Noto‘g‘ri yoki eskirgan tasdiqlash havolasi!")
        return redirect("register")


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]  # username -> email
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            send_mail(
                "Kirish muvaffaqiyatli!",
                f"Hurmatli {user.username}, siz Alibaba.com tizimiga muvaffaqiyatli kirdingiz!",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect("product_list")
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri!")
            return redirect("login")

    return render(request, "education/Authentication/login.html")


def user_logout(request):
    if request.user.is_authenticated:
        send_mail(
            "Chiqish amalga oshirildi!",
            f"Hurmatli {request.user.username}, siz Alibaba.com tizimidan chiqdingiz!",
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
    logout(request)
    return redirect("product_list")