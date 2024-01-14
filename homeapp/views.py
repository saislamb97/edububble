from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, TextbookStatusForm
from .decorators import student_required, staff_required
from django.contrib import messages
from .models import ClassName, TextbookStatus, Student, Textbook, update_available_quantity, User
from django.db.models import Count
import plotly.express as px
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# User Index Views
@login_required(login_url='homeapp:login')
@staff_required
def IndexView(request):
    user = request.user

    textbookstatusform = TextbookStatusForm()
    classes = ClassName.objects.all()
    class_students_textbooks = []
    selected_class = None
    selected_student = None
    section_name = None

    chart_data_for_classes = []
    for class_obj in classes:
        chart_data = generate_textbook_status_chart_for_class(class_obj)
        chart_data_for_classes.append(chart_data)

    if request.method == 'POST':
        if 'statusform' in request.POST:
            textbookstatusform = TextbookStatusForm(request.POST)
            if textbookstatusform.is_valid():
                # Update textbook status
                update_textbook_status(request)
                # Retrieve and display data for the selected class_id after update
                selected_class = get_object_or_404(ClassName, id=request.POST.get('selected_class_id'))
                section_name = request.POST.get('selected_section_id')
                student_id = request.POST.get('student_id')
                selected_student = get_object_or_404(Student, id=student_id)
                class_students_textbooks = retrieve_students_by_class_and_section(selected_class, section_name)

        elif 'section_student_form' in request.POST:
            # Form submission to filter students by class ID and section name
            selected_class = get_object_or_404(ClassName, id=request.POST.get('selected_class_id'))
            section_name = request.POST.get('selected_section_id')
            student_id = request.POST.get('student_id')
            selected_student = get_object_or_404(Student, id=student_id)
            class_students_textbooks = retrieve_students_by_class_and_section(selected_class, section_name)
            
        elif 'class_section_form' in request.POST:
            # Form submission to filter students by class ID and section name
            class_section_id = request.POST.get('class_section_id')
            section_name = request.POST.get('section_name')
            selected_class = get_object_or_404(ClassName, id=class_section_id)
            class_students_textbooks = retrieve_students_by_class_and_section(selected_class, section_name)

        elif 'class_id' in request.POST:
            # Retrieve and display data for the selected class_id
            selected_class = get_object_or_404(ClassName, id=request.POST.get('class_id'))
            class_students_textbooks = retrieve_class_data(selected_class)

    context = {
        'user': user,
        'class_students_textbooks': class_students_textbooks,
        'textbookstatusform': textbookstatusform,
        'selected_class': selected_class,
        'selected_student':selected_student,
        'selected_section': section_name,
        'all_classes': classes,
        'chart_data_for_classes': chart_data_for_classes,
    }

    return render(request, 'index.html', context)

@login_required(login_url='homeapp:login')
@student_required
def StudentIndexView(request):
    user = request.user
    classes = ClassName.objects.all()
    student = None
    selected_class = None

    chart_data_for_classes = []
    for class_obj in classes:
        chart_data = generate_textbook_status_chart(class_obj, user)
        chart_data_for_classes.append(chart_data)

    # Query the Students model using the logged-in user
    try:
        student = Student.objects.get(username=user)
    except Student.DoesNotExist:
        # Handle case where the student doesn't exist for the logged-in user
        print("Student information not found.")

    # Retrieve student profile or return 404 if it doesn't exist
    student_profile = get_object_or_404(Student, username=user)
    user_textbooks = student_profile.textbooks.all()
    textbooks_with_status = []

    if request.method == 'POST' and 'class_id' in request.POST:
        # Retrieve the selected class
        selected_class = get_object_or_404(ClassName, id=request.POST.get('class_id'))

        # Filter textbooks based on the selected class without modifying user_textbooks
        textbooks_for_class = Textbook.objects.filter(classname=selected_class)

        for textbook in user_textbooks:
            if textbook in textbooks_for_class:  # Check if the textbook belongs to the selected class
                class_name = textbook.classname.classname
                textbook_status = TextbookStatus.objects.filter(student=student_profile, textbook=textbook).first()
                status = 'Not Collected'  # Default status if no textbook status found
                if textbook_status:
                    status = 'Collected' if textbook_status.collected else ('Returned' if textbook_status.returned else 'Not Collected')

                textbooks_with_status.append({
                    'textbook': textbook,
                    'class_name': class_name,
                    'status': status
                })

    context = {
        'textbooks_with_status': textbooks_with_status,
        'selected_class': selected_class,
        'user': user,
        'all_classes': classes,
        'student': student,
        'chart_data_for_classes': chart_data_for_classes,
    }
    return render(request, 'student_index.html', context)

@login_required(login_url='homeapp:login')
@staff_required
def AllTextbookView(request):
    textbooks_by_class = {}
    all_textbooks = Textbook.objects.all()
    textbooks_by_class = {}

    # Group textbooks by classname
    for textbook in all_textbooks:
        class_name = getattr(textbook.classname, 'classname', None)
        if class_name:
            if class_name not in textbooks_by_class:
                textbooks_by_class[class_name] = []
            textbooks_by_class[class_name].append(textbook)
        else:
            print(f"Skipping textbook with ID {textbook.id} as classname is None.")

    return render(request, 'alltextbook.html', {'textbooks_by_class': textbooks_by_class})

def generate_textbook_status_chart(class_name, user):
    class_textbooks = Textbook.objects.filter(classname=class_name)

    collected_count = TextbookStatus.objects.filter(textbook__in=class_textbooks, student__username=user, collected=True).count()
    returned_count = TextbookStatus.objects.filter(textbook__in=class_textbooks, student__username=user, returned=True).count()
    not_collected_count = class_textbooks.count() - (collected_count + returned_count)

    counts = {
        'class_name': class_name.classname,
        'collected': collected_count,
        'returned': returned_count,
        'not_collected': not_collected_count
    }

    fig = px.pie(values=list(counts.values()), names=list(counts.keys()), title=class_name.classname)
    fig.update_traces(textinfo='percent+label', hole=0.4)

    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return {
        'chart_div': chart_div,
        'counts': counts
    }


def generate_textbook_status_chart_for_class(class_name):
    # Retrieve all students in the specified class
    students_in_class = Student.objects.filter(classname=class_name)

    # Initialize counts
    collected_count = 0
    returned_count = 0
    not_collected_count = 0

    # Loop through each student
    for student in students_in_class:
        # Retrieve textbooks for the current student assigned to the specified class
        textbooks_for_student_in_class = student.textbooks.filter(classname=class_name)

        # Check the status of each textbook for the current student
        for textbook in textbooks_for_student_in_class:
            # Try to get the status for the current student and textbook
            textbook_status = TextbookStatus.objects.get(student=student, textbook=textbook)

            # Update counts based on the status
            if textbook_status.collected:
                collected_count += 1
            elif textbook_status.returned:
                returned_count += 1
            else:
                not_collected_count += 1

    # Prepare counts dictionary
    counts = {
        'class_name': class_name.classname,
        'collected': collected_count,
        'returned': returned_count,
        'not_collected': not_collected_count
    }

    # Create pie chart
    fig = px.pie(values=list(counts.values()), names=list(counts.keys()), title=class_name.classname)
    fig.update_traces(textinfo='percent+label', hole=0.4)

    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return {
        'chart_div': chart_div,
        'counts': counts
    }

def retrieve_students_by_class_and_section(selected_class, section_name):
    # Retrieve students that match the given class ID and section name
    students = Student.objects.filter(classname=selected_class, section=section_name)
    class_students_textbooks = []

    sections = Student.objects.filter(classname=selected_class).values_list('section', flat=True).distinct()

    for section in sections:
        section_students = students.filter(section=section)
        class_students = []

        for student in section_students:
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

def retrieve_class_data(selected_class):
    class_students_textbooks = []
    sections = Student.objects.filter(classname=selected_class).values_list('section', flat=True).distinct()

    for section in sections:
        students = Student.objects.filter(classname=selected_class, section=section)
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

def update_textbook_status(request):
    # Extract and update textbook status
    student_id = request.POST.get('student_id')
    textbook_id = request.POST.get('textbook_id')
    collected = request.POST.get('collected')
    returned = request.POST.get('returned')

    student = get_object_or_404(Student, id=student_id)
    textbook = get_object_or_404(Textbook, id=textbook_id)
    textbook_status = get_object_or_404(TextbookStatus, student=student, textbook=textbook)

    # Update status based on checkbox selections
    textbook_status.collected = collected is not None
    textbook_status.returned = returned is not None
    textbook_status.save()

    # Call the update_available_quantity logic after saving TextbookStatus
    update_available_quantity(sender=TextbookStatus, instance=textbook_status)

    messages.success(request, 'Textbook status updated.')

def generate_student_report(student, textbooks_status):
    # Function to generate the content of the PDF report
    template = get_template('student_index.html')
    context = {'student': student, 'textbooks_status': textbooks_status}
    content = template.render(context)
    return content

def student_report_pdf(request, student_id, class_name):
    # Get the student object
    student = get_object_or_404(Student, student_id=student_id)

    # Fetch textbooks and their status for the specific class
    textbooks_status = TextbookStatus.objects.filter(student=student, textbook__classname__classname=class_name)

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.username.fullname}_report.pdf"'

    # Create PDF document using reportlab
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

   # Header
    header = student.username.fullname
    header_style = getSampleStyleSheet()['Heading1']
    header_style.alignment = 1  # 0 for left, 1 for center, 2 for right

    elements.append(Paragraph(header, header_style))

    # Student Information Table
    student_info_data = [
        ["Full Name", student.username.fullname],
        ["Student ID/IC", student.student_id],
        ["Class Name", student.classname.classname],
        ["Section", student.section],
    ]
    student_info_table = Table(student_info_data, colWidths=[120, 200])
    student_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(student_info_table)

    # Textbooks Table
    textbooks_data = [["Title", "Collected", "Returned"]]
    textbooks_data += [[
        ts.textbook.book_title,
        "Yes" if ts.collected else "No",
        "Yes" if ts.returned else "No"
    ] for ts in textbooks_status]

    textbooks_table = Table(textbooks_data, colWidths=[300, 80, 80])
    textbooks_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('NOBREAK', (0, 0), (-1, -1), 1),  # Avoid page break within the table
    ]))
    elements.append(textbooks_table)

    # Build the PDF
    pdf.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()

    response.write(pdf_content)
    return response

def LoginView(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('homeapp:student_index')
        else:
            return redirect('homeapp:index')

    if request.method == 'POST':
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            user = loginform.get_user()
            login(request, user)
            if user.is_student:
                return redirect('homeapp:student_index')
            else:
                return redirect('homeapp:index')
    else:
        loginform = LoginForm()

    return render(request, 'login.html', {'loginform': loginform})


def LogoutView(request):
    logout(request)
    return redirect('homeapp:login')