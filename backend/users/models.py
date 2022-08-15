from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

class User(AbstractUser):
    ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    username = models.CharField(max_length=50,
                                unique=True,
                                )
    email = models.EmailField(max_length=50,
                              unique=True,
                              )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','first_name','last_name']

    class Meta:
        verbose_name = 'пользователь'

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username

