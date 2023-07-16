from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
import uuid


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("users must have an email adress")
        if not username:
            raise ValueError("users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username , password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username= username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key = True,default=uuid.uuid4,editable=False)

    Genders=[
        ("Male","Male"),
        ("Female","Female")
    ]

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=7,choices=Genders,default = "Male")
    phone_num = PhoneNumberField(blank=True)
    current_residence = CountryField(null =True , blank = True)
    nationality = CountryField(null =True , blank = True)
    
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_active = models.BooleanField(default=True)

    # For staff members
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    profile_image = models.URLField(default="https://www.freeiconspng.com/thumbs/account-icon/account-icon-33.png")
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'username',
    ]

    objects = MyAccountManager()
    
    class Meta:
        unique_together = ('username','email')

    def __str__(self):
        return f"<a href='/accounts/{self.id}'>@{self.username}</a>"
    
    def get_full_name(self):
        full_name = "%s" % (self.username,)
        return full_name.strip()