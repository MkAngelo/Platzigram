"""Users models."""

# Django
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField


class Profile(models.Model):
    """Profile model.
    
    Proxy model that extends the base data with other information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to='user/pictures',
        blank = True,
        null = True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username

class Following(models.Model):
    """Following of the user."""
    user = models.OneToOneField(User, on_delete=CASCADE)
    followed = models.ManyToManyField(User, related_name='followed')

    @classmethod
    def follow(cls,user,another_account):
        obj, create = cls.objects.get_or_create()
        obj.followed.add(another_account)

    @classmethod
    def unfollow(cls,user,another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)

    def __str__(self):
        # return str(self.user)
        return self.user.username