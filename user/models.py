from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import EmailValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CaseInsensitiveEmailField(models.EmailField):
    description = "Email (case-insensitive)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(EmailValidator(message='Enter a valid email address.'))

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            return value.lower()
        return value
    
class User(AbstractUser):
    email = CaseInsensitiveEmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    
class FriendRequest(models.Model):
    REQUESTED = 0
    ACCEPTED = 1
    REJECTED = 2
    REQUEST_STATUS = (
        (REQUESTED, 'Requested'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendrequestuser')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendrequesttouser')
    created = models.DateTimeField('created', auto_now_add=True)
    status = models.SmallIntegerField('status', default=0, choices=REQUEST_STATUS)
    modified = models.DateTimeField('modified', auto_now_add=True)


    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.status}"