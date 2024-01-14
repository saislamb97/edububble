from django import forms
from django.contrib import admin
from .models import User, ClassName, Textbook, Student, TextbookStatus, update_available_quantity
from django.contrib.auth.admin import UserAdmin
from django.db import transaction

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

    update_to_form1_class.short_description = "Update selected textbooks to Form1 class"
    update_to_form2_class.short_description = "Update selected textbooks to Form2 class"
    update_to_form3_class.short_description = "Update selected textbooks to Form3 class"
    update_to_form4_class.short_description = "Update selected textbooks to Form4 class"
    update_to_form5_class.short_description = "Update selected textbooks to Form5 class"

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

    # Add the following line to enable checkbox option for textbooks
    filter_horizontal = ('textbooks',)
    
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
    search_fields = ['student__student_id', 'student__username__username', 'textbook__book_title']
    list_filter = ['student__classname', 'collected', 'returned']

    actions = ['mark_as_collected', 'mark_as_returned', 'uncheck_collected_returned']

    @transaction.atomic
    def mark_as_collected(self, request, queryset):
        queryset.update(collected=True, returned=False)
        self.update_available_quantity(queryset)

    mark_as_collected.short_description = "Mark selected as collected"

    @transaction.atomic
    def mark_as_returned(self, request, queryset):
        queryset.update(collected=False, returned=True)
        self.update_available_quantity(queryset)

    mark_as_returned.short_description = "Mark selected as returned"

    @transaction.atomic
    def uncheck_collected_returned(self, request, queryset):
        queryset.update(collected=False, returned=False)
        self.update_available_quantity(queryset)

    uncheck_collected_returned.short_description = "Uncheck both collected and returned"

    def update_available_quantity(self, queryset):
        for instance in queryset:
            update_available_quantity(sender=TextbookStatus, instance=instance)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Filter textbooks based on the classes assigned to students
        student_classes = queryset.values_list('student__classname', flat=True).distinct()
        queryset = queryset.filter(textbook__classname__in=student_classes)

        return queryset, use_distinct

# Change the title of the Django admin site
admin.site.site_header = 'SMK ORKID DESA Admin Panel'
admin.site.site_title = 'SMK ORKID DESA || Admin'
admin.site.index_title = 'Admin Dashboard'

admin.site.register(User, UserAdminConfig)
admin.site.register(ClassName,ClassNameConfig)
admin.site.register(Textbook, TextbooksConfig)
admin.site.register(Student,StudentConfig)
admin.site.register(TextbookStatus,TextbookStatusConfig)
