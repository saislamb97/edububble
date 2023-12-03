from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, TextbookStatusForm, UserForm
from .decorators import admin_required, student_required, staff_required
from django.contrib import messages
from .models import ClassName, TextbookStatus, Students, Textbooks


# User Index Views
@login_required(login_url='homeapp:login')
@admin_required
def IndexView(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'index.html', context)

@login_required(login_url='homeapp:login')
@student_required
def StudentIndexView(request):
    user = request.user
    
    # Retrieve student profile or return 404 if it doesn't exist
    student_profile = get_object_or_404(Students, username=user)
    user_textbooks = student_profile.textbooks.all()
    
    textbooks_with_status = []
    for textbook in user_textbooks:
        class_name = textbook.classname.classname  # Access classname directly from ForeignKey
        # Retrieve the corresponding TextbookStatus instance if it exists
        textbook_status = TextbookStatus.objects.filter(student=student_profile, textbook=textbook).first()
        status = 'Not Specified'  # Default status if no textbook status found
        if textbook_status:
            if textbook_status.collected:
                status = 'Collected'
            elif textbook_status.returned:
                status = 'Returned'
        
        textbooks_with_status.append({
            'textbook': textbook,
            'class_name': class_name,
            'status': status
        })
    
    context = {
        'textbooks_with_status': textbooks_with_status,
        'user': user,
    }
    return render(request, 'student_index.html', context)

@login_required(login_url='homeapp:login')
@staff_required
def StaffIndexView(request):
    textbookstatusform = TextbookStatusForm()
    classes = ClassName.objects.all()
    class_students_textbooks = []
    selected_class = None
    section_name = None

    if request.method == 'POST':
        if 'statusform' in request.POST:
            textbookstatusform = TextbookStatusForm(request.POST)
            if textbookstatusform.is_valid():
                # Update textbook status
                update_textbook_status(request)
                # Retrieve and display data for the selected class_id after update
                selected_class = get_object_or_404(ClassName, id=request.POST.get('selected_class_id'))
                section_name = request.POST.get('selected_section_id')
                class_students_textbooks = retrieve_students_by_class_and_section(selected_class, section_name)
            
        elif 'class_id' in request.POST:
            # Retrieve and display data for the selected class_id
            selected_class = get_object_or_404(ClassName, id=request.POST.get('class_id'))
            class_students_textbooks = retrieve_class_data(selected_class)

        elif 'class_section_form' in request.POST:
            # Form submission to filter students by class ID and section name
            class_section_id = request.POST.get('class_section_id')
            section_name = request.POST.get('section_name')
            selected_class = get_object_or_404(ClassName, id=class_section_id)
            class_students_textbooks = retrieve_students_by_class_and_section(selected_class, section_name)

    context = {
        'class_students_textbooks': class_students_textbooks,
        'textbookstatusform': textbookstatusform,
        'selected_class': selected_class,
        'selected_section': section_name,
        'all_classes': classes,
    }

    return render(request, 'staff_index.html', context)

def retrieve_students_by_class_and_section(selected_class, section_name):
    # Retrieve students that match the given class ID and section name
    students = Students.objects.filter(classname=selected_class, section=section_name)
    class_students_textbooks = []

    for student in students:
        textbooks = student.textbooks.all()
        textbooks_with_status = []

        for textbook in textbooks:
            textbook_status, _ = TextbookStatus.objects.get_or_create(student=student, textbook=textbook)
            textbooks_with_status.append({
                'textbook': textbook,
                'status': textbook_status,
            })

        class_students_textbooks.append({
            'class_obj': selected_class,
            'class_students': [{
                'student': student,
                'textbooks': textbooks_with_status,
            }],
        })

    return class_students_textbooks

def update_textbook_status(request):
    # Extract and update textbook status
    student_id = request.POST.get('student_id')
    textbook_id = request.POST.get('textbook_id')
    collected = request.POST.get('collected')
    returned = request.POST.get('returned')

    student = get_object_or_404(Students, id=student_id)
    textbook = get_object_or_404(Textbooks, id=textbook_id)
    textbook_status = get_object_or_404(TextbookStatus, student=student, textbook=textbook)

    # Update status based on checkbox selections
    textbook_status.collected = collected is not None
    textbook_status.returned = returned is not None
    textbook_status.save()

    messages.success(request, 'Textbook status updated.')

def retrieve_class_data(selected_class):
    class_students_textbooks = []
    sections = Students.objects.filter(classname=selected_class).values_list('section', flat=True).distinct()

    for section in sections:
        students = Students.objects.filter(classname=selected_class, section=section)
        class_students = []

        for student in students:
            textbooks = student.textbooks.all()
            textbooks_with_status = []

            for textbook in textbooks:
                textbook_status, _ = TextbookStatus.objects.get_or_create(student=student, textbook=textbook)
                textbooks_with_status.append({
                    'textbook': textbook,
                    'status': textbook_status,
                })

            class_students.append({
                'student': student,
                'textbooks': textbooks_with_status,
            })

        class_students_textbooks.append({
            'class_obj': selected_class,
            'section': section,
            'class_students': class_students,
        })

    return class_students_textbooks

# User Profile and Login Views
@login_required(login_url='homeapp:login')
def UserProfileView(request):
    user = request.user
    userform = UserForm(instance=user)

    if request.method == 'POST':
        userform = UserForm(request.POST, instance=user)
        if userform.is_valid():
            userform.save()
            messages.success(request, 'Your information was successfully updated.')
            return redirect('homeapp:userprofile')

    context = {
        'userform': userform,
    }

    return render(request, 'userprofile.html', context)

def LoginView(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('homeapp:index')
        elif request.user.is_student:
            return redirect('homeapp:student_index')
        elif request.user.is_staff:
            return redirect('homeapp:staff_index')
        else:
            return redirect('homeapp:index')

    if request.method == 'POST':
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            user = loginform.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('homeapp:index')
            elif user.is_student:
                return redirect('homeapp:student_index')
            elif user.is_staff:
                return redirect('homeapp:staff_index')
            else:
                return redirect('homeapp:index')
    else:
        loginform = LoginForm()

    return render(request, 'login.html', {'loginform': loginform})


def LogoutView(request):
    logout(request)
    return redirect('homeapp:login')