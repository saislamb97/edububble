from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed, pre_save
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
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
    
    def clean(self):
        # Check if the user has multiple roles selected
        roles_count = sum([self.is_student, self.is_teacher])

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
    
class TextbookStatus(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbooks, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('collected', 'Collected'),
        ('not_collected', 'Not Collected'),
        ('returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    previous_status = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.textbook.book_title} - {self.status}"
    
@receiver(m2m_changed, sender=Students.textbooks.through)
def create_student_textbook(sender, instance, action, **kwargs):
    if action == 'post_add':
        textbooks = kwargs['pk_set']
        for textbook_id in textbooks:
            textbook = get_object_or_404(Textbooks, id=textbook_id)
            TextbookStatus.objects.create(student=instance, textbook=textbook, status='not_collected')

@receiver(post_save, sender=TextbookStatus)
def textbook_status_changed(sender, instance, **kwargs):
    if not kwargs.get('created'):  # Send notifications on updates
        user_email = instance.student.username.email
        status = instance.status
        old_status = instance.previous_status  # Retrieve the previous status from the model field
        if status != old_status:
            if status == 'collected':
                send_collect_notification(user_email)
            elif status == 'returned':
                send_return_notification(user_email)

@receiver(pre_save, sender=TextbookStatus)
def track_previous_status(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance already exists (update operation)
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance.previous_status = old_instance.status  # Track the previous status before saving
        except sender.DoesNotExist:
            print("The instance does not exist yet.")


def send_collect_notification(email):
    subject = 'Textbook Status Changed'
    message = 'You have collected your book.'
    send_mail(subject, message, 'sa.islamb97@gmail.com', [email])

def send_return_notification(email):
    subject = 'Textbook Status Changed'
    message = 'You have returned your book.'
    send_mail(subject, message, 'sa.islamb97@gmail.com', [email])