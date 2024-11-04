from django import forms
from django.utils import timezone
from .models import *
from datetime import timedelta


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'user', 'dob', 'sex', 'blood_type', 'marital_status',
            'city', 'address', 'state', 'pin_code', 'phoneNo',
            'email', 'emergencyContactName', 'emergencyContactPhone',
            'emergencyContactRelation', 'medical_history', 'allergies'
        ]



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time'] 

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = CustomUser.objects.filter(user_type='doctor')
        
        self.fields['date'].widget.attrs.update({
            'min': timezone.now().date().isoformat(),
            'max': (timezone.now() + timedelta(days=3)).date().isoformat()
        })

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if doctor and date and time:
            if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
                raise forms.ValidationError('The selected time slot is already booked.')

        return cleaned_data

    def get_available_time_slots(self, doctor, date):
        """Fetch available time slots for a given doctor on a specified date."""
        all_slots = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00']
        booked_times = Appointment.objects.filter(doctor=doctor, date=date).values_list('time', flat=True)
        available_slots = [slot for slot in all_slots if slot not in booked_times]
        return available_slots
        


class AppointmentFilterForm(forms.Form):
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Select Date'
    )
