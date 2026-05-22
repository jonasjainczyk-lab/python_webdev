# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # This inherits username, password, email, first_name, last_name, etc.
    # We can also add a profile field here if desired:
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

