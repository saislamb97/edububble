from django.db import models
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
import random

def generate_unique_id():
    # Generate a random 6-digit unique ID
    unique_id = random.randint(100000, 999999)
    return unique_id

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
    is_student = models.BooleanField(default=False)
    is_library = models.BooleanField(default=False)
    is_finance = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
    
    def clean(self):
        # Check if the user has multiple roles selected
        roles_count = sum([self.is_student, self.is_library, self.is_finance])

        if roles_count > 1:
            raise ValidationError("A user cannot have multiple roles simultaneously.")

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation before saving
        super().save(*args, **kwargs)

class ClassName(models.Model):
    CLASS_CHOICES = [
        ('form1', 'Form 1'),
        ('form2', 'Form 2'),
        ('form3', 'Form 3'),
        ('form4', 'Form 4'),
        ('form5', 'Form 5'),
    ]
    classname = models.CharField(max_length=250, choices=CLASS_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.classname
    
class Textbooks(models.Model):
    book_title = models.CharField(max_length=250)
    book_id = models.CharField(max_length=250, default=generate_unique_id, unique=True)
    classname = models.ForeignKey(ClassName, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.book_title

class Students(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=250, default=generate_unique_id, unique=True)
    classname = models.ForeignKey(ClassName, on_delete=models.SET_NULL, null=True)
    SECTION_CHOICES = [
        ('sec_a', 'Section A'),
        ('sec_b', 'Section B'),
        ('sec_c', 'Section C'),
        ('sec_d', 'Section D'),
        ('sec_e', 'Section E'),
    ]
    section = models.CharField(max_length=250, blank=True, null=True, choices=SECTION_CHOICES)
    total_credit = models.IntegerField(blank=True, null=True)
    total_due = models.IntegerField(blank=True, null=True)
    textbooks = models.ManyToManyField(Textbooks, blank=True)

    def __str__(self):
        return str(self.username)
    
@receiver(post_save, sender=User)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    if instance.is_student:
        # Check if the user is marked as a student
        if created:
            # If the User instance is newly created and marked as a student
            Students.objects.create(username=instance)
        else:
            # If the User instance is updated and marked as a student,
            # get the associated Students instance and update it
            student_profile, _ = Students.objects.get_or_create(username=instance)
            # Update other fields if needed
            student_profile.save()
    else:
        # If the user is not marked as a student, delete the associated Students instance
        Students.objects.filter(username=instance).delete()

@receiver(post_save, sender=User)
def delete_student_profile(sender, instance, **kwargs):
    if not instance.is_student:
        # If the user is not marked as a student, delete the associated Students instance
        Students.objects.filter(username=instance).delete()
    
class StudentTextbook(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbooks, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('collected', 'Collected'),
        ('not_collected', 'Not Collected'),
        ('returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.username} - {self.textbook.book_title} - {self.status}"
    
@receiver(m2m_changed, sender=Students.textbooks.through)
def create_student_textbook(sender, instance, action, **kwargs):
    if action == 'post_add':
        textbooks = kwargs['pk_set']
        for textbook_id in textbooks:
            textbook = Textbooks.objects.get(id=textbook_id)
            StudentTextbook.objects.create(student=instance, textbook=textbook, status='not_collected')

def payslip_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Supported extensions are .jpg, .jpeg, .png, .pdf')

class PaymentApplication(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    application_id = models.CharField(max_length=250, default=generate_unique_id, unique=True)
    application_date = models.DateTimeField(default=timezone.now)
    paying_amount = models.IntegerField()
    payslip = models.FileField(upload_to='payslips/', validators=[payslip_file_extension])
    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student)
    
    def clean(self):
        # Check if the application has multiple statuses selected
        statuses_count = sum([self.is_pending, self.is_approved, self.is_rejected])

        if statuses_count > 1:
            raise ValidationError("A payment application cannot have multiple statuses simultaneously.")

    def save(self, *args, **kwargs):
        
        # Check if the application is approved
        if self.is_approved:
            # Update the related Students model
            self.student.total_due -= self.paying_amount
            self.student.total_credit += self.paying_amount
            self.student.save()

        super(PaymentApplication, self).save(*args, **kwargs)

@receiver(post_save, sender=PaymentApplication)
def payment_application_changed(sender, instance, **kwargs):
    # Check if the approval status changed
    user_email = instance.student.username.email 
    if getattr(instance, '_original_is_approved', False) != instance.is_approved:
        send_approval_notification(user_email)
    elif getattr(instance, '_original_is_rejected', False) != instance.is_rejected:
        send_rejection_notification(user_email)

# Save the original values when the instance is loaded
@receiver(post_save, sender=PaymentApplication)
def save_original_values(sender, instance, **kwargs):
    instance._original_is_approved = instance.is_approved
    instance._original_is_rejected = instance.is_rejected

def send_approval_notification(email):
    # Implement your email sending logic here for approval notification
    subject = 'Payment Application Approved'
    message = 'Your payment application has been approved.'
    send_mail(subject, message, 'sa.islamb97@gmail.com', [email])

def send_rejection_notification(email):
    # Implement your email sending logic here for rejection notification
    subject = 'Payment Application Rejected'
    message = 'Your payment application has been rejected.'
    send_mail(subject, message, 'sa.islamb97@gmail.com', [email])