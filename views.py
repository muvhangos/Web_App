from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
import uuid

# Temporary in-memory token store
tokens = {}

def home(request):
    return render(request, "main/home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User inactive until email verification
            user.save()
            token = str(uuid.uuid4())
            tokens[token] = user.username
            send_mail(
                "Verify Your Email",
                f"Click here to verify: http://127.0.0.1:8000/verify/{token}",
                "no-reply@example.com",
                [user.email],
                fail_silently=False,
            )
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "main/register.html", {"form": form})

def verify_email(request, token):
    username = tokens.get(token)
    if username:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        return redirect("login")
    return redirect("home")

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "main/dashboard.html")

def logout_user(request):
    logout(request)
    return redirect("home")
