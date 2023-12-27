from django import forms
from django.contrib import admin
from .models import User, ClassName, Textbook, Student, TextbookStatus
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
    list_display = ('username', 'fullname', 'email', 'is_student', 'is_staff', 'is_active')
    search_fields = ('username', 'fullname', 'email')

class ClassNameConfig(admin.ModelAdmin):
    model = ClassName
    search_fields = ['classname', 'description']
    list_display = ['classname', 'description']
    list_filter = ['classname', 'description']

class TextbooksConfig(admin.ModelAdmin):
    model = Textbook
    search_fields = ['book_title', 'classname__classname']
    list_display = ['book_title', 'book_id', 'classname', 'quantity_total', 'available_quantity']
    list_filter = ['classname']

    # Actions to update students' class to different choices
    def update_to_form1_class(self, request, queryset):
        self.update_class(request, queryset, 'Form1')

    def update_to_form2_class(self, request, queryset):
        self.update_class(request, queryset, 'Form2')

    def update_to_form3_class(self, request, queryset):
        self.update_class(request, queryset, 'Form3')

    def update_to_form4_class(self, request, queryset):
        self.update_class(request, queryset, 'Form4')

    def update_to_form5_class(self, request, queryset):
        self.update_class(request, queryset, 'Form5')

    def update_class(self, request, queryset, class_name):
        selected_class = ClassName.objects.get(classname=class_name)
        queryset.update(classname=selected_class)

    update_to_form1_class.short_description = "Update selected students to Form1 class"
    update_to_form2_class.short_description = "Update selected students to Form2 class"
    update_to_form3_class.short_description = "Update selected students to Form3 class"
    update_to_form4_class.short_description = "Update selected students to Form4 class"
    update_to_form5_class.short_description = "Update selected students to Form5 class"

    actions = [
        'update_to_form1_class', 'update_to_form2_class', 'update_to_form3_class',
        'update_to_form4_class', 'update_to_form5_class',
    ]

class StudentConfig(admin.ModelAdmin):
    model = Student
    list_display = ['username', 'get_full_name', 'student_id', 'classname', 'section']

    def get_full_name(self, obj):
        return obj.username.fullname
    get_full_name.short_description = 'Full Name'

    search_fields = ['username__username', 'username__fullname', 'student_id', 'classname__classname', 'section']
    list_filter = ['classname', 'section']
    
    # Actions to update students' class to different choices
    def update_to_form1_class(self, request, queryset):
        self.update_class(request, queryset, 'Form1')

    def update_to_form2_class(self, request, queryset):
        self.update_class(request, queryset, 'Form2')

    def update_to_form3_class(self, request, queryset):
        self.update_class(request, queryset, 'Form3')

    def update_to_form4_class(self, request, queryset):
        self.update_class(request, queryset, 'Form4')

    def update_to_form5_class(self, request, queryset):
        self.update_class(request, queryset, 'Form5')

    def update_to_graduate_class(self, request, queryset):
        self.update_class(request, queryset, 'Graduate')

    def update_class(self, request, queryset, class_name):
        selected_class = ClassName.objects.get(classname=class_name)
        queryset.update(classname=selected_class)

    update_to_form1_class.short_description = "Update selected students to Form1 class"
    update_to_form2_class.short_description = "Update selected students to Form2 class"
    update_to_form3_class.short_description = "Update selected students to Form3 class"
    update_to_form4_class.short_description = "Update selected students to Form4 class"
    update_to_form5_class.short_description = "Update selected students to Form5 class"
    update_to_graduate_class.short_description = "Update selected students to Graduate class"

    actions = [
        'update_to_form1_class', 'update_to_form2_class', 'update_to_form3_class',
        'update_to_form4_class', 'update_to_form5_class', 'update_to_graduate_class'
    ]

class TextbookStatusConfig(admin.ModelAdmin):
    model = TextbookStatus
    list_display = ['student', 'textbook', 'collected', 'returned']
    search_fields = ['student__username__username', 'textbook__book_title']
    list_filter = ['textbook__classname', 'collected', 'returned']

# Change the title of the Django admin site
admin.site.site_header = 'SMK ORKID DESA Admin Panel'
admin.site.site_title = 'SMK ORKID DESA || Admin'
admin.site.index_title = 'Admin Dashboard'

admin.site.register(User, UserAdminConfig)
admin.site.register(ClassName,ClassNameConfig)
admin.site.register(Textbook, TextbooksConfig)
admin.site.register(Student,StudentConfig)
admin.site.register(TextbookStatus,TextbookStatusConfig)
