from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        
        # Create the user instance
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        
        # Create the user instance
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    fullname = models.CharField(max_length=250, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
    
def payslip_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']  # Add other valid extensions as needed
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Supported extensions are .jpg, .jpeg, .png, .pdf')

class PaymentApplication(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payslip = models.FileField(upload_to='payslips/', validators=[payslip_file_extension])
    is_approved = models.BooleanField(default=False)

class PaymentApproval(models.Model):
    application = models.ForeignKey(PaymentApplication, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

class PaymentRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid_month = models.DateField()
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s PaymentRecord for {self.paid_month}"
    
class LibraryBooks(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    classname = models.CharField(max_length=250)