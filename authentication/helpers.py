from typing import List
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from pydantic import BaseModel
import random
import requests
# Define Pydantic
class ValidationResult(BaseModel):
    message: str
    status: bool
    error_messages: List[str]

def is_valid_email(email: str) -> bool:
    try:
        # Use Django's validate_email to check if the email is valid
        validate_email(email)
        return True
    except ValidationError:
        return False

def check_email(email: str) -> ValidationResult:
    if is_valid_email(email):
        return ValidationResult(
            message="Valid email", 
            status=True, 
            error_messages=[]
        )
    else:
        return ValidationResult(
            message="Invalid email", 
            status=False, 
            error_messages=['Please enter a valid email address']
        )

def is_valid_password(password: str) -> ValidationResult:
    try:
        # Use Django's validate_password to check if the password is valid
        validate_password(password)
        return ValidationResult(
            message="Valid password", 
            status=True, 
            error_messages=[]
        )
    except ValidationError as e:
        # If validation fails, we can print or handle the error messages
        error_messages = [message for message in e.messages]
        return ValidationResult(
            message="Invalid password", 
            status=False, 
            error_messages=error_messages
        )

# Generate user 6 digits code


def generate_6_digit_code():
    return str(random.randint(100000, 999999))


def send_registration_code_mail(url, code):
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, data={"userCode": code}, headers=headers)
        return response.status_code
    except:
        return 400




