
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from .utils import generate_verification_link

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            link = request.build_absolute_uri(generate_verification_link(user))
            send_mail("Verify Email", f"Click to verify: {link}", None, [user.email])
            return render(request, "check_email.html")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def verify_email(request, token):
    signer = TimestampSigner()
    User = get_user_model()
    try:
        unsigned = signer.unsign(token, max_age=86400)
        user = User.objects.get(pk=unsigned)
        user.email_verified=True
        user.is_active=True
        user.save()
        return render(request,"verified_success.html")
    except SignatureExpired:
        return render(request,"verified_failed.html",{"error":"Expired"})
    except:
        return render(request,"verified_failed.html",{"error":"Invalid"})
