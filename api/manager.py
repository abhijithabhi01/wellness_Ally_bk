from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, phone, full_name, dob, gender, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(
            phone=phone,
            full_name=full_name,
            dob=dob,
            gender=gender,
            email=email,
            **extra_fields
        )
        user.password = make_password(password)  # Encrypt the password before saving
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(phone, password, **extra_fields)

      