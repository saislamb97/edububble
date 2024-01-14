from django.urls import path
from homeapp import views

app_name = 'homeapp'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('student/', views.StudentIndexView, name='student_index'),
    path('alltextbook', views.AllTextbookView, name='alltextbook'),
    path('student_report/<str:student_id>/<str:class_name>/', views.student_report_pdf, name='student_report_pdf'),
]