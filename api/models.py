from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    full_name = models.CharField(max_length=60,blank=False,null=False)
    phone=models.CharField(max_length=13,blank=False,null=False,unique=True)
    dob=models.CharField(max_length=20,blank=False,null=False)
    email=models.EmailField(max_length=200,null=True,blank=True)
    gender=models.CharField(max_length=20,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ROLE_CHOICES = (    
        ('admin', 'Admin'),
        ('patient','Patient')
    )
    user_type = models.CharField(max_length=20,default='patient', choices=ROLE_CHOICES)
   

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.phone}{self.full_name}"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff



class HealthCondition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class HealthIssues(models.Model):
    issue = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='health_issue',null=True,blank=True)

    def __str__(self):
        return self.issue


class HealthProfile(models.Model):
    condition = models.ForeignKey(HealthCondition,on_delete = models.CASCADE)
    issue = models.ForeignKey(HealthIssues,on_delete = models.CASCADE)
    description = description = models.TextField(null=True ,blank= True)

    def __str__(self):
        return f"{self.issue.issue} --{self.condition.name}"


class DietPlans(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    health_profile = models.ForeignKey(HealthProfile,on_delete = models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class ExerciseVideos(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    health_profile = models.ForeignKey(HealthProfile,on_delete = models.CASCADE)
    image = models.ImageField(upload_to='exercise_videos',null=True,blank=True)
    video = models.FileField(upload_to='exercise_videos', null=True, blank=True) 
    def __str__(self):
        return f"{self.name}"

class SymptomTips(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='symptom',null=True,blank=True)
    health_profile = models.ForeignKey(HealthProfile,on_delete = models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='category',null=True,blank=True)
    health_profile = models.ForeignKey(HealthProfile,on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category.name}--{self.name}"