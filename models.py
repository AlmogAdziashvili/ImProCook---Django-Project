from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, title, create_time, profile_pic, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            create_time=create_time,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            title=title,
            profile_pic=profile_pic,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, title, create_time, profile_pic, password):
        user = self.create_user(
            email,
            create_time=create_time,
            password=password,
            first_name=first_name,
            last_name=last_name,
            title=title,
            profile_pic=profile_pic,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    create_time = models.DateField(default=now)
    profile_pic = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Follow(models.Model):
    id          = models.BigAutoField(primary_key=True)
    following_pk = models.IntegerField()
    user_pk     = models.IntegerField()
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.following_pk) + " follows " + str(self.user_pk)

    def __unicode__(self):
        return str(self.following_pk) + " follows " + str(self.user_pk)