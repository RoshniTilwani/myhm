import django_tables2 as tables
from .models import MedicalRecord

class PatientTable(tables.Table):
    patient_name = tables.Column(accessor='patient.username', verbose_name='Patient Name')

    class Meta:
        model = MedicalRecord
        template_name = "django_tables2/bootstrap.html" 
        fields = ("patient_name", "medical_history", "diagnosis", "treatment_plan", "prescription", "record_date")
