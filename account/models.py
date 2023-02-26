from django.db import models
import uuid
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=155, blank=True, null=True)
    phone = models.CharField(max_length=155, blank=True, null=True)
    photo = models.ImageField(upload_to="media/profile", height_field=None, width_field=None, max_length=100, blank=True, null=True)
    email = models.CharField(max_length=155, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    user = models.OneToOneField("auth.User",on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=155, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        date = datetime.now()
        self.date_added = date
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        db_table = "account_profile"
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        ordering = ('date_added',)


    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.phone




