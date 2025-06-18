
import random
import string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))


# Function to check if the input is a valid email
def is_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False