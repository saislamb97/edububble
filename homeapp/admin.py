from django import forms
from django.contrib import admin
from .models import LibraryBooks, PaymentApplication, User, PaymentApproval, PaymentRecord, Textbooks, Students, Class, ClassName
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

# Custom form for user creation in the admin panel
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'fullname', 'password1', 'password2', 'is_staff', 'is_active')


class UserAdminConfig(UserAdmin):
    add_form = CustomUserCreationForm

    search_fields = ('email', 'username', 'fullname')
    list_filter = ('email', 'username', 'fullname', 'is_active', 'is_staff')
    ordering = ('email',)
    list_display = ('email', 'username', 'fullname', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'fullname', 'start_date')}),
        ('Permission', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'fullname', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

class PaymentApplicationConfig(admin.ModelAdmin):
    model = PaymentApplication
    search_fields = ('title',)
    list_display = ('title', 'description', 'user', 'is_approved')

class PaymentApprovalConfig(admin.ModelAdmin):
    model = PaymentApproval
    search_fields = ('application', 'approved_by',)
    list_display = ('application', 'approved_by', 'approved_at')

class PaymentRecordConfig(admin.ModelAdmin):
    model = PaymentRecord
    search_fields = ('user', 'paid_month',)
    list_display = ('user', 'paid_month', 'is_paid')

class LibraryBooksConfig(admin.ModelAdmin):
    model = LibraryBooks
    search_fields = ('title', 'classname',)
    list_display = ('title', 'description', 'classname')

class TextbookConfig(admin.ModelAdmin):
    model = Textbooks
    search_fields = ['title']
    list_display = ['title', 'classname', 'quantity']

class StudentConfig(admin.ModelAdmin):
    list_display = ['name', 'email', 'classname', 'section', 'student_id', 'status']
    search_fields = ['name', 'email', 'student_id']
    list_filter = ['classname', 'section', 'status']
    
class ClassConfig(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    
class ClassNameConfig(admin.ModelAdmin):
    search_fields = ['classname', 'section']
    list_display = ['classname', 'section', 'textbooks']
    list_filter = ['classname', 'section']


# Register the User model with the custom UserAdminConfig
admin.site.register(User, UserAdminConfig)
admin.site.register(PaymentApplication, PaymentApplicationConfig)
admin.site.register(PaymentApproval, PaymentApprovalConfig)
admin.site.register(PaymentRecord, PaymentRecordConfig)
admin.site.register(LibraryBooks, LibraryBooksConfig)
admin.site.register(Textbooks, TextbookConfig)
admin.site.register(Students,StudentConfig)
admin.site.register(Class,ClassConfig)
admin.site.register(ClassName,ClassNameConfig)
