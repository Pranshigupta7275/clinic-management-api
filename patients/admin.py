from django.contrib import admin
from .models import Patient, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'gender', 'contact_number']
    search_fields = ['name', 'contact_number']
    list_filter = ['gender', 'blood_group']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor_name', 'appointment_date', 'status']
    search_fields = ['doctor_name', 'patient__name', 'patient__contact_number'] # Added contact search
    list_filter = ['status', 'appointment_date']
    list_editable = ['status']  
    date_hierarchy = 'appointment_date' 