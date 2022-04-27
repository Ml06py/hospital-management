from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class BaseUser(AbstractUser):
    # base info
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique=True,blank=True,null=True)
    picture = models.ImageField(blank=True,null=True, upload_to="profiles/")
    birthday = models.DateField(blank=True,null=True)
    user_id = models.PositiveIntegerField(unique=True,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    token = models.CharField(max_length=15,null=True,blank=True,unique=True)
    #Doctor stuff
    doctor_id = models.PositiveIntegerField(blank=True,unique=True,null=True)
    # hospital = models.ForeignKey(hospital,on_delete=CASCADE)
    more_info = models.TextField(blank=True,null=True)

    class status(models.TextChoices):
        patient = ("pa","patient")
        superuser = ("su","superuser")
        admin = ("ad","admin")
        doctor = ("do","doctor")
    user_status = models.CharField(max_length=2,choices=status.choices,default=status.patient)
    # permissions
    add_hospital = models.BooleanField(default=False)
    add_doctor = models.BooleanField(default=False)
    add_admin = models.BooleanField(default=False)

