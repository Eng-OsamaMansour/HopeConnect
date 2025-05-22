from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Role(models.TextChoices):
    ADMIN      = "ADMIN",  _("Admin")        
    DONOR      = "DONOR",  _("Donor")       
    ORPHANAGE  = "ORPHAN", _("Orphanage")    
    VOLUNTEER  = "VOLUN",  _("Volunteer")    
    LOGISTICS  = "LOGIS",  _("Logistics")    

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("role",       Role.ADMIN)
        extra_fields.setdefault("is_staff",   True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active",  True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"),  max_length=150, blank=True)
    last_name = models.CharField(_("last name"),   max_length=150, blank=True)
    role = models.CharField( _("role"),max_length=20,choices=Role.choices,default=Role.DONOR,)
    phone_number = models.CharField(_("phone number"), max_length=30, blank=True)
    is_staff = models.BooleanField(_("staff status"),default=False,help_text=_("Designates whether the user can log into the admin site."),)
    is_active = models.BooleanField(_("active"),default=True,help_text=_("Unselect this instead of deleting accounts to disable a user."),)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["role"]
    class Meta:
        verbose_name        = _("user")
        verbose_name_plural = _("users")
        ordering            = ("-date_joined",)
    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self) -> str:
        return self.first_name or self.email.split("@")[0]
