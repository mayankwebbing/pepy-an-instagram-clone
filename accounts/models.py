from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator
from accounts.validators import MinAgeValidator, UsernameValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import uuid
# Create your models here.

class ProfileManager(BaseUserManager):
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def get_queryset(self):
        return super().get_queryset()

    def exclude_self(self, profile):
        return self.get_queryset().exclude(id=profile.id)

class Profile(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('empty', 'Prefer not to say'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(max_length=30, unique=True, validators=[UsernameValidator()])
    full_name = models.CharField(max_length=65)

    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile/', default='profile/defaultpic.png', blank=True)
    cover_img = models.ImageField(upload_to='profile/', blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, blank=True)
    website = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(validators=[MinAgeValidator(12)], null=True, blank=True, default=None)
    followers = models.ManyToManyField('self', blank=True, related_name='following', symmetrical=False)
    fcm_token = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)

    is_deleted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, blank=True, related_name='profile_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='profile_users')

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f'@{self.username} Profile'

class ChangeUsername(models.Model):
    user_id = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    new_username = models.CharField(max_length=30, validators=[UsernameValidator()])
    old_username = models.CharField(max_length=30, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=14)
        if ChangeUsername.objects.filter(user_id = self.user_id, updated_at__range = (start_date, end_date)).count() > 1:
            raise ValidationError("Cannot change username more than 2 times in 2 weeks")
        elif Profile.objects.filter(username = self.new_username).count() > 0:
            raise ValidationError("Username already Exist")

        self.old_username = self.user_id.username
        self.user_id.username = self.new_username
        self.user_id.save()

        if not self.old_username:
            raise ValidationError("Try back again")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'@{self.old_username} changed to @{self.new_username}'