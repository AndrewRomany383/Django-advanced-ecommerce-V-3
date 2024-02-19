from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if email is None:
            raise ValueError('your email is required')
        if username is None:
            raise ValueError('your name is required')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_anonymous = False
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    username = models.CharField(max_length=30, unique=True)
    phonenumber = models.CharField(max_length=13)
    email = models.EmailField(max_length=50, unique=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='userprofile', blank=True)
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.full_name}'

    @property
    def profile_picture_url(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url

















