
from django.core.signing import TimestampSigner
from django.urls import reverse
signer = TimestampSigner()

def generate_verification_link(user):
    token = signer.sign(user.pk)
    return reverse("verify_email", kwargs={"token": token})
