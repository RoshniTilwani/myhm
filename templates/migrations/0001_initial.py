# Generated by Django 5.0.6 on 2024-11-01 08:17

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=50)),
                ('no_doctors', models.IntegerField(default=0)),
                ('no_staff', models.IntegerField(default=0)),
                ('dept_phone', models.CharField(max_length=12)),
                ('floor_number', models.IntegerField(default=1)),
                ('specialty', models.CharField(max_length=100)),
                ('background_image', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(choices=[('General', 'General'), ('Single', 'Single'), ('Double', 'Double'), ('ICU', 'ICU'), ('VIP', 'VIP')], max_length=10)),
                ('room_floor', models.IntegerField(default=1)),
                ('avl_status', models.CharField(choices=[('Vacant', 'Vacant'), ('Occupied', 'Occupied'), ('Under Maintenance', 'Under Maintenance')], default='Vacant', max_length=20)),
                ('room_rate_per_day', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('staff', 'Staff'), ('admin', 'Admin')], default='patient', max_length=10)),
                ('dob', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdmittedPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admit_date', models.DateField()),
                ('discharge_date', models.DateField(blank=True, null=True)),
                ('medProcedure', models.CharField(default='General Checkup', max_length=100)),
                ('reason_for_admission', models.TextField()),
                ('treatment_plan', models.TextField()),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admitted_patients_doctor', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admitted_patients', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='templates.room')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_mode', models.CharField(default='Not Paid', max_length=20)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('mode', models.CharField(default='In-Person', max_length=20)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('payment_mode', models.CharField(choices=[('Online', 'Online'), ('Cash', 'Cash'), ('Cheque', 'Cheque'), ('Credit Card', 'Credit Card')], default='Cash', max_length=20)),
                ('admission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billings', to='templates.admittedpatient')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(default='General Physician', max_length=100)),
                ('education', models.CharField(default='MBBS', max_length=200)),
                ('experience', models.CharField(default='0 years', max_length=50)),
                ('fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='templates.dept')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eq_name', models.CharField(max_length=50)),
                ('qty', models.IntegerField(default=0)),
                ('purchase_yr', models.PositiveIntegerField(default=2024)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('maintenance_status', models.CharField(choices=[('Working', 'Working'), ('Under Repair', 'Under Repair'), ('Out of Service', 'Out of Service')], default='Working', max_length=20)),
                ('next_maintenance', models.DateField(default=django.utils.timezone.now)),
                ('dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='templates.dept')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_history', models.TextField()),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('treatment_plan', models.TextField(blank=True, null=True)),
                ('prescription', models.TextField(blank=True, null=True)),
                ('record_date', models.DateField(default=django.utils.timezone.now)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_records_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=6)),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], default='O+', max_length=3)),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], default='Single', max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=20)),
                ('pin_code', models.CharField(max_length=10)),
                ('phoneNo', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
                ('emergencyContactName', models.CharField(max_length=50)),
                ('emergencyContactPhone', models.CharField(max_length=12)),
                ('emergencyContactRelation', models.CharField(max_length=50)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('medical_history', models.TextField()),
                ('allergies', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to='templates.dept')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_role', models.CharField(choices=[('Nurse', 'Nurse'), ('Receptionist', 'Receptionist'), ('Administrator', 'Administrator'), ('Pharmacist', 'Pharmacist'), ('Technician', 'Technician')], default='Nurse', max_length=20)),
                ('salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('staff_shift', models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening'), ('Night', 'Night')], default='Morning', max_length=10)),
                ('phoneNo', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=100)),
                ('dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='templates.dept')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('doctor', 'date', 'time'), name='unique_appointment'),
        ),
    ]