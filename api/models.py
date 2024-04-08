from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError
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
    description = models.TextField(null=True ,blank= True)
    image = models.ImageField(upload_to='health-profile',null=True,blank=True)

    def __str__(self):
        return f"{self.issue.issue} --{self.condition.name}"

class DietPlans(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    health_profile = models.ForeignKey(HealthProfile,on_delete = models.CASCADE)
    image = models.ImageField(upload_to='dietplans',null=True,blank=True)
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
        return f"{self.health_profile}--{self.name}"

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField(default='10')
    is_out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category.name}--{self.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(default='0',max_digits=10, decimal_places=2)
    payed = models.BooleanField(default=False)
    address = models.TextField(default='no address')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"Order #{self.id} - {self.user.full_name}"
 
class CommunityChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class PersonalChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    replay = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.full_name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
   
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)  # Corrected typo

    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_time.strftime('%Y-%m-%d %H:%M:%S')}"

    def is_time_slot_available(self):
        # Check if there is any appointment at the same time
        conflicting_appointments = Appointment.objects.filter(
            appointment_time=self.appointment_time
        ).exclude(pk=self.pk)

        if conflicting_appointments.exists():
            raise ValidationError("Appointment time slot is not available.")

    def save(self, *args, **kwargs):
        self.is_time_slot_available()  
        super().save(*args, **kwargs)
