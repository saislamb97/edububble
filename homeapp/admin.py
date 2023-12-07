from django import forms
from django.contrib import admin
from .models import User, ClassName, Textbooks, Students, TextbookStatus
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'fullname', 'start_date')}),
        ('Permissions', {'fields': ('is_student', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_student', 'is_staff'),
        }),
    )
    list_display = ('username', 'email', 'fullname', 'is_student', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'fullname')

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
    list_display = ['username', 'student_id', 'classname', 'section']
    search_fields = ['username__username', 'student_id', 'classname__classname', 'section']
    list_filter = ['classname', 'section']
    form = StudentAdminForm

class TextbookStatusConfig(admin.ModelAdmin):
    model = TextbookStatus
    list_display = ['student', 'textbook', 'collected', 'returned']
    search_fields = ['student__username', 'textbook__book_title']
    list_filter = ['student', 'textbook', 'collected', 'returned']

# Change the title of the Django admin site
admin.site.site_header = 'SMK ORKID DESA Admin Panel'
admin.site.site_title = 'SMK ORKID DESA || Admin'
admin.site.index_title = 'Admin Dashboard'

admin.site.register(User, UserAdminConfig)
admin.site.register(ClassName,ClassNameConfig)
admin.site.register(Textbooks, TextbooksConfig)
admin.site.register(Students,StudentConfig)
admin.site.register(TextbookStatus,TextbookStatusConfig)
