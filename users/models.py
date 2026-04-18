import pathlib
import uuid
from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager


class UserManager(DjangoUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def user_image_file_path(instance: "User", filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.name)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("uploads/users/") / pathlib.Path(filename)


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"), max_length=63, unique=True, null=True, blank=True
    )
    bio = models.TextField(_("bio"), null=True, blank=True)
    avatar = models.ImageField(null=True, upload_to=user_image_file_path)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
