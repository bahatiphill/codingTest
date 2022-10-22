from django.db import models


class Users(models.Model):

    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'NA'),
    ]

    names = models.CharField(max_length=100, null=True, blank=True)
    nid = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER ,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_valid = models.BooleanField(default=False)
    nid_valid = models.BooleanField(default=False)
    email_valid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.names