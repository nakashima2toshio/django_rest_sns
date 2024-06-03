# accounts/models.py
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission, \
#     AbstractUser
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('メールアドレスは必須です')
#
#         email = self.normalize_email(email)
#         email = email.lower()
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         user = self.create_user(email, password, **extra_fields)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user
#
#
# class UserAccount(AbstractUser):
#     # 既存のフィールドとメソッドを保持
#     email = models.EmailField("email", max_length=255, unique=True)
#     username = models.CharField("username", max_length=255, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     class Meta:
#         verbose_name = 'User_Account'
#
#     # related_nameを追加して修正
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_name="useraccount_set",
#         related_query_name="useraccount",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user_permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="useraccount_set",
#         related_query_name="useraccount",
#     )
#
#     def __str__(self):
#         return self.email
