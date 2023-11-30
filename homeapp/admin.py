from django import forms
from django.contrib import admin
from .models import User, ClassName, Textbooks, Students, PaymentApplication, StudentTextbook
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

# Custom form for user creation in the admin panel
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'fullname', 'password1', 'password2')


class UserAdminConfig(UserAdmin):
    add_form = CustomUserCreationForm

    search_fields = ('email', 'username', 'fullname')
    list_filter = ('is_student', 'is_library', 'is_finance', 'is_staff', 'is_active')
    ordering = ('email', 'username')
    list_display = ('email', 'username', 'fullname', 'is_student', 'is_library', 'is_finance', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'fullname', 'start_date')}),
        ('Permission', {'fields': ('is_student', 'is_library', 'is_finance', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'fullname', 'password1', 'password2')}
         ),
    )

class ClassNameConfig(admin.ModelAdmin):
    model = ClassName
    search_fields = ['classname', 'description']
    list_display = ['classname', 'description']
    list_filter = ['classname', 'description']

class TextbooksConfig(admin.ModelAdmin):
    model = Textbooks
    search_fields = ['book_title', 'book_id', 'classname']
    list_display = ['book_title', 'book_id', 'classname']
    list_filter = ['book_title', 'book_id', 'classname']

class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentAdminForm, self).__init__(*args, **kwargs)
        # Filter available textbooks based on the selected class
        self.fields['textbooks'].queryset = self.fields['textbooks'].queryset.filter(classname=self.instance.classname)

class StudentConfig(admin.ModelAdmin):
    model = Students
    list_display = ['username', 'student_id', 'classname', 'section', 'total_credit', 'total_due']
    search_fields = ['username__username', 'student_id', 'classname__classname', 'section']
    list_filter = ['username', 'student_id', 'classname', 'section']
    form = StudentAdminForm

class StudentTextbookConfig(admin.ModelAdmin):
    model = StudentTextbook
    list_display = ['student', 'textbook', 'status']
    search_fields = ['student__username', 'textbook__book_title']
    list_filter = ['student', 'textbook', 'status']

class PaymentApplicationConfig(admin.ModelAdmin):
    model = PaymentApplication
    list_display = ['student', 'application_date', 'paying_amount', 'is_pending', 'is_approved', 'is_rejected']
    search_fields = ['student__username', 'application_date', 'paying_amount', 'is_pending', 'is_approved', 'is_rejected']
    list_filter = ['student', 'application_date', 'paying_amount', 'is_pending', 'is_approved', 'is_rejected']

# Change the title of the Django admin site
admin.site.site_header = 'SMK ORKID DESA Admin Panel'
admin.site.site_title = 'SMK ORKID DESA || Admin'
admin.site.index_title = 'Admin Dashboard'

admin.site.register(User, UserAdminConfig)
admin.site.register(ClassName,ClassNameConfig)
admin.site.register(Textbooks, TextbooksConfig)
admin.site.register(Students,StudentConfig)
admin.site.register(StudentTextbook,StudentTextbookConfig)
admin.site.register(PaymentApplication, PaymentApplicationConfig)
