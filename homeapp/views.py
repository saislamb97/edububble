from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm
from .decorators import admin_required, student_required, teacher_required
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

    if user.is_authenticated and user.is_student:
        student_profile = Students.objects.get(username=user)
        user_textbooks = student_profile.textbooks.all()
        
        # Fetch class names for the textbooks along with their status
        textbooks_with_status = []
        for textbook in user_textbooks:
            class_name = ClassName.objects.get(pk=textbook.classname_id)
            # Retrieve the corresponding StudentTextbook instance
            student_textbook = TextbookStatus.objects.filter(student=student_profile, textbook=textbook).first()
            textbooks_with_status.append({
                'textbook': textbook,
                'class_name': class_name.classname,
                'status': student_textbook.status if student_textbook else 'Not Specified'
            })
        
        context = {
            'textbooks_with_status': textbooks_with_status,
            'user': user,
        }


    return render(request, 'student_index.html', context)

@login_required(login_url='homeapp:login')
@teacher_required
def teacherIndexView(request):
    user = request.user
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        textbook_id = request.POST.get('textbook_id')
        status = request.POST.get('status')

        student = get_object_or_404(Students, id=student_id)
        textbook = get_object_or_404(Textbooks, id=textbook_id)
        student_textbook = get_object_or_404(TextbookStatus, student=student, textbook=textbook)

        # Update the status
        student_textbook.status = status
        student_textbook.save()
        messages.success(request, 'Textbook status updated.')

        # Redirect or handle the response as needed
        return redirect('homeapp:teacher_index')

    classes = ClassName.objects.all()
    class_students_textbooks = []

    for class_obj in classes:
        students = Students.objects.filter(classname=class_obj)
        class_students = []

        for student in students:
            textbooks = student.textbooks.all()
            textbooks_with_status = []
            
            for textbook in textbooks:
                student_textbook = TextbookStatus.objects.filter(student=student, textbook=textbook).first()
                textbooks_with_status.append({
                    'textbook': textbook,
                    'status': student_textbook.status if student_textbook else 'Not Specified'
                })
            
            class_students.append({
                'student': student,
                'textbooks': textbooks_with_status
            })

        class_students_textbooks.append({
            'class_obj': class_obj,
            'class_students': class_students
        })

    context = {
        'class_students_textbooks': class_students_textbooks,
        'user': user,
    }

    return render(request, 'teacher_index.html', context)

# User Profile and Login Views
@login_required(login_url='homeapp:login')
def UserProfileView(request):
    user = request.user
    userform = UserForm(instance=user)

    if request.method == 'POST':
        if 'userform-submit' in request.POST:
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
        elif request.user.is_teacher:
            return redirect('homeapp:teacher_index')
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
            elif user.is_teacher:
                return redirect('homeapp:teacher_index')
            else:
                return redirect('homeapp:index')
    else:
        loginform = LoginForm()

    return render(request, 'login.html', {'loginform': loginform})


def LogoutView(request):
    logout(request)
    return redirect('homeapp:login')