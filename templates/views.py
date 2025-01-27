from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import DetailView,ListView
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from datetime import date
from .forms import AppointmentForm ,AppointmentFilterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from datetime import date
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from datetime import datetime 
from django.views.generic import ListView
from django_filters.views import FilterView
from django.db.models import Q
from .tables import PatientTable
from .filters import PatientFilter
from django_tables2 import SingleTableMixin

#  Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()
def logout_view(request):
    logout(request)
    return redirect('login') 

def home(request):
    departments = Dept.objects.all()  
    return render(request, 'templates/home.html', {'departments': departments})

@login_required
def doctorDashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('login') 

    return render(request, 'templates/doctorDashboard.html', {'doctor': doctor})

def appointment_success(request):
     departments = Dept.objects.all()
     return render(request,'templates/appointment_success.html')




def registerAsPatient(request):
    if request.method == 'POST':
        print("Form data received:", request.POST)

        patient_data = {
            'first_name': request.POST.get('fname'),  
            'last_name': request.POST.get('lname'),  
            'dob': request.POST.get('dob'),
            'sex': request.POST.get('sex'),
            'blood_type': request.POST.get('bloodType'),
            'marital_status': request.POST.get('marital_status'),
            'city': request.POST.get('city'),
            'address': request.POST.get('address'),
            'state': request.POST.get('state'),
            'pin_code': request.POST.get('pincode'), 
            'phoneNo': request.POST.get('phoneNo'), 
            'email': request.POST.get('email'),
            'emergencyContactName': request.POST.get('emergencyContactName'),  
            'emergencyContactPhone': request.POST.get('emergencyContactPhone'), 
            'emergencyContactRelation': request.POST.get('emergencyContactRelation'),  
            'medical_history': request.POST.get('medical_history'),
            'allergies': request.POST.get('allergies'),
        }

        username = request.POST.get('username')  
        password = request.POST.get('password')

        print(f"Username: {username}, Password: {password}")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'templates/registerAsPatient.html')

        try:
            with transaction.atomic():  
                print("Creating user...")
                user = CustomUser.objects.create_user(
                    username=username,
                    email=patient_data['email'],
                    password=password,  
                    first_name=patient_data['first_name'],  
                    last_name=patient_data['last_name'],   
                    user_type='patient',
                    dob=patient_data['dob'],  
                )
                print("User created successfully:", user)

                
                patient = Patient.objects.create(
                    user=user,  
                    dob=patient_data['dob'],
                    sex=patient_data['sex'],
                    blood_type=patient_data['blood_type'],
                    marital_status=patient_data['marital_status'],
                    city=patient_data['city'],
                    address=patient_data['address'],
                    state=patient_data['state'],
                    pin_code=patient_data['pin_code'],
                    phoneNo=patient_data['phoneNo'],
                    email=patient_data['email'],
                    emergencyContactName=patient_data['emergencyContactName'],
                    emergencyContactPhone=patient_data['emergencyContactPhone'],
                    emergencyContactRelation=patient_data['emergencyContactRelation'],
                    medical_history=patient_data['medical_history'],
                    allergies=patient_data['allergies'],
                )

                print("Patient record created successfully")
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('main-home') 
        except Exception as e:
            print("Error occurred during registration:", str(e))
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'templates/registerAsPatient.html')

    return render(request, 'templates/registerAsPatient.html')


@login_required(login_url='login')  
def medicalRecord(request):
    try:
        patient = Patient.objects.get(user=request.user)

        today = date.today()
        age = today.year - patient.dob.year - ((today.month, today.day) < (patient.dob.month, patient.dob.day))
        
        records = MedicalRecord.objects.filter(patient=request.user)
        departments = Dept.objects.all()
        return render(request, 'templates/medicalRecord.html', {'departments': departments,'records': records, 'patient': patient, 'age': age})
    
    except Patient.DoesNotExist:
        return render(request, 'templates/errorpage.html', {'message': 'No medical record found.'})


@login_required
def patientDashboard(request):
    print("Logged in user:", request.user)  
    departments = Dept.objects.all()
    try:
        patient = Patient.objects.get(user=request.user)
        print("Patient found:", patient) 

        context = {
            'patient': patient,
            'departments': departments
        }

        return render(request, 'templates/patientDashboard.html', context)
    except Patient.DoesNotExist:
        print("No patient record found for user:", request.user)  
        return render(request, 'templates/errorPage.html', {'message': 'No patient record found for this user.'})



class DeptDetailView(DetailView):
    model = Dept
    template_name = 'templates/dept_detail.html'  
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = self.object.doctors.all() 
        context['procedures'] = self.object.procedures.all() 
        context['departments'] = Dept.objects.all()
        return context


class DeptListView(ListView):
    model = Dept
    template_name = 'dept_list.html'
    context_object_name = 'departments'



def login_view(request):
    if request.method == 'POST':
        print("Form submitted")  

        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        print("Username:", username) 
        print("Password:", password)   
        print("User Type:", user_type)  

        if not (username and password and user_type):
            messages.error(request, 'Please fill all fields.')
            return render(request, 'templates/login.html')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                if user_type == 'Patient':
                    return redirect('patientDashboard')
                elif user_type == 'doctor':
                    return redirect('doctorDashboard')
                elif user_type == 'staff':
                    return redirect('staffDashboard')
            else:
                messages.error(request, 'Invalid username or password.')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            print("Error:", str(e))  

    return render(request, 'templates/login.html')



def department_list(request):
    departments = Dept.objects.all()  
    return render(request, 'templates/department_list.html', {'departments': departments})

def department_detail(request, dept_id):
    department = get_object_or_404(Dept, id=dept_id)
    return render(request, 'templates/department_detail.html', {'department': department})

@login_required(login_url='login')
def bookAnAppointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  
            appointment.mode = 'In-Person'     
            appointment.payment_mode = 'Not Paid'  
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'templates/bookAnAppointment.html', {'form': form})


@login_required
def get_available_times(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')

    if doctor_id and date:
        doctor = CustomUser.objects.get(id=doctor_id)
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        all_slots = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00']
        
        booked_times = Appointment.objects.filter(doctor=doctor, date=date_obj).values_list('time', flat=True)
        booked_slots = {slot.strftime("%H:%M") for slot in booked_times}
        
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        
        return JsonResponse({'available_slots': available_slots})

    return JsonResponse({'available_slots': []})

def department_detail(request, pk):
    dept = get_object_or_404(Dept, pk=pk)
    
    doctors = dept.doctors.all()
    procedures = dept.procedures.all()
    
    return render(request, 'templates/department_detail.html', {
        'dept': dept,
        'doctors': doctors,
        'procedures': procedures
    })


def docApp(request):
    form = AppointmentFilterForm(request.GET or None)
    appointments = []

    if request.user.is_authenticated and request.user.user_type == 'doctor':
        selected_date = form.cleaned_data['date'] if form.is_valid() else timezone.now().date()
        appointments = Appointment.objects.filter(doctor=request.user, date=selected_date)
    
    return render(request, 'templates/docApp.html', {'form': form, 'appointments': appointments})


def staffDashboard(request):
    staff = get_object_or_404(Staff, user=request.user)

    context = {
        'staff': staff,
    }
    return render(request, 'templates/staffDashboard.html', context)

class PatientRecordView(SingleTableMixin, FilterView):
    model = MedicalRecord
    table_class = PatientTable
    template_name = "templates/patient_records.html"
    filterset_class = PatientFilter  

    def get_queryset(self):
        queryset = super().get_queryset()  
        doctor = self.request.user  
        queryset = queryset.filter(doctor=doctor)
        return queryset  


# @login_required(login_url='login')
# def docMedRec(request):
#     user = request.user
#     search_query = request.GET.get('search', '')

#     records = MedicalRecord.objects.filter(
#         doctor=user
#     ).filter(
#         Q(patient__first_name__icontains=search_query) |
#         Q(patient__last_name__icontains=search_query) |
#         Q(patient__username__icontains=search_query)
#     ).select_related('patient')

#     return render(request, 'templates/docMedRec.html', {
#         'records': records,
#         'search_query': search_query  
#     })
