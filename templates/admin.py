from django.contrib import admin
from .models import (
    CustomUser,
    Patient,
    Dept,
    Doctor,
    Staff,
    Procedure,
    Appointment,
    Room,
    AdmittedPatient,
    Billing,
    MedicalRecord,
    Equipments,
)

# Register your models here
admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Dept)
admin.site.register(Doctor)
admin.site.register(Staff)
admin.site.register(Procedure)
admin.site.register(Appointment)
admin.site.register(Room)
admin.site.register(AdmittedPatient)
admin.site.register(Billing)
admin.site.register(MedicalRecord)
admin.site.register(Equipments)
