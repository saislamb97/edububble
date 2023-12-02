from django.urls import path
from homeapp import views

app_name = 'homeapp'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('login/', views.LoginView, name='login'),
    path('userprofile/', views.UserProfileView, name='userprofile'),
    path('logout/', views.LogoutView, name='logout'),
    path('student/', views.StudentIndexView, name='student_index'),
    path('teacher/', views.teacherIndexView, name='teacher_index'),
]