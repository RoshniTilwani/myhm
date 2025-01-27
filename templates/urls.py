from django.urls import path,include
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from .views import get_available_times

urlpatterns = [
    path('', views.home,name='main-home'),
    path('login', views.login_view, name='login'),
    path('bookAnAppointment', views.bookAnAppointment,name='bookAnAppointment'),
    path('appointment_success', views.appointment_success,name='appointment_success'),
    path('get_available_times', views.get_available_times, name='get_available_times'),
    path('registerAsPatient', views.registerAsPatient,name='registerAsPatient'),
    path('medicalRecord', views.medicalRecord,name='medicalRecord'),
    path('patientDashboard', views.patientDashboard,name='patientDashboard'),
    path('doctorDashboard', views.doctorDashboard,name='doctorDashboard'),
    path('staffDashboard', views.staffDashboard,name='staffDashboard'),
    path('docApp/', views.docApp, name='docApp'),
    path('staffDashboard', staffDashboard, name='staffDashboard'),
    path('departments/', DeptListView.as_view(), name='departments'),
    path('department/<int:pk>/', DeptDetailView.as_view(), name='dept_detail'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='main-home'), name='logout'),
    path('logout/', logout_view, name='lgout'),
    path('docMedRec', views.PatientRecordView.as_view(), name='docMedRec'),
]