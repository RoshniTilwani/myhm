from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    dob = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    def __str__(self):
        return self.username


class Patient(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patients', null=True, blank=True)
    dob = models.DateField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default='Other')  
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, default='O+') 
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')  
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=12)
    email = models.EmailField()
    emergencyContactName = models.CharField(max_length=50)
    emergencyContactPhone = models.CharField(max_length=12)
    emergencyContactRelation = models.CharField(max_length=50)
    registration_date = models.DateField(auto_now_add=True)
    medical_history = models.TextField()
    allergies = models.TextField()

    def __str__(self):
        return self.user.username


class Dept(models.Model):
    id = models.AutoField(primary_key=True)  
    dept_name = models.CharField(max_length=50)
    no_doctors = models.IntegerField(default=0)  
    no_staff = models.IntegerField(default=0)  
    dept_phone = models.CharField(max_length=12)
    floor_number = models.IntegerField(default=1)  
    specialty = models.CharField(max_length=100)
    background_image = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.dept_name

    def get_absolute_url(self):
        return reverse('dept-detail', kwargs={'pk': self.pk})


class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctors', null=True, blank=True)
    position = models.CharField(max_length=100, default='General Physician')  
    education = models.CharField(max_length=200, default='MBBS')  
    experience = models.CharField(max_length=50, default='0 years') 
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    department = models.ForeignKey(Dept, on_delete=models.CASCADE, related_name='doctors', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


STAFF_ROLE_CHOICES = [
    ('Nurse', 'Nurse'),
    ('Receptionist', 'Receptionist'),
    ('Administrator', 'Administrator'),
    ('Pharmacist', 'Pharmacist'),
    ('Technician', 'Technician'),
]
SHIFT_CHOICES = [
    ('Morning', 'Morning'),
    ('Evening', 'Evening'),
    ('Night', 'Night'),
]

class Staff(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='staffs', null=True, blank=True)
    staff_role = models.CharField(max_length=20, choices=STAFF_ROLE_CHOICES, default='Nurse') 
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    staff_shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, default='Morning') 
    phoneNo = models.CharField(max_length=12)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Procedure(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    department = models.ForeignKey(Dept, on_delete=models.CASCADE, related_name='procedures', null=True, blank=True)

    def __str__(self):
        return self.name



class Appointment(models.Model):
    id = models.AutoField(primary_key=True)  
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_as_patient', null=True, blank=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_as_doctor', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    payment_mode = models.CharField(max_length=20, default='Not Paid')
    status = models.CharField(max_length=20, default='Pending')
    mode = models.CharField(max_length=20, default='In-Person')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'date', 'time'], name='unique_appointment')
        ]

    def save(self, *args, **kwargs):
        if not self.patient or not self.doctor:
            raise ValueError("Patient and Doctor must be specified")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Appointment {self.id} - {self.patient.first_name} {self.patient.last_name} with {self.doctor.username} on {self.date} at {self.time}'


class Room(models.Model):
    id = models.AutoField(primary_key=True)  
    ROOM_TYPE_CHOICES = [
        ('General', 'General'),
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('ICU', 'ICU'),
        ('VIP', 'VIP'),
    ]
    AVL_STATUS_CHOICES = [
        ('Vacant', 'Vacant'),
        ('Occupied', 'Occupied'),
        ('Under Maintenance', 'Under Maintenance'),
    ]

    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    room_floor = models.IntegerField(default=1)  
    avl_status = models.CharField(max_length=20, choices=AVL_STATUS_CHOICES, default='Vacant') 
    room_rate_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  

    def __str__(self):
        return f"Room {self.id} - {self.room_type}"


class AdmittedPatient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admitted_patients', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    admit_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    medProcedure = models.CharField(max_length=100, default='General Checkup')  
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admitted_patients_doctor', null=True, blank=True)
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    reason_for_admission = models.TextField()
    treatment_plan = models.TextField()

    @property
    def patient_name(self):
        return self.user.username  

    def __str__(self):
        return f"Admitted {self.user.username}"


class Billing(models.Model):
    id = models.AutoField(primary_key=True)  
    BILL_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]
    PAYMENT_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Credit Card', 'Credit Card'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='billings', null=True, blank=True)
    admission = models.ForeignKey(AdmittedPatient, on_delete=models.CASCADE, related_name='billings', null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    status = models.CharField(max_length=10, choices=BILL_STATUS_CHOICES, default='Pending')
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='Cash')

    @property
    def bill_status(self):
        return self.status

    def __str__(self):
        return f"Billing for {self.patient.username} - {self.total_amount} ({self.status})"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_records', null=True, blank=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_records_doctor', null=True, blank=True)
    medical_history = models.TextField()
    diagnosis = models.TextField(null=True, blank=True)
    treatment_plan = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    record_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Medical Record for {self.patient.username} on {self.record_date}"


class Equipments(models.Model):
    id = models.AutoField(primary_key=True)  
    MAINTENANCE_STATUS_CHOICES = [
        ('Working', 'Working'),
        ('Under Repair', 'Under Repair'),
        ('Out of Service', 'Out of Service'),
    ]
    
    eq_name = models.CharField(max_length=50)
    qty = models.IntegerField(default=0)  
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, related_name='equipments', null=True, blank=True)
    purchase_yr = models.PositiveIntegerField(default=timezone.now().year) 
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    maintenance_status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS_CHOICES, default='Working')  
    next_maintenance = models.DateField(default=timezone.now)  

    def __str__(self):
        return self.eq_name
    
