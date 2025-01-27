# filters.py
import django_filters
from django.db.models import Q
from .models import MedicalRecord

class PatientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search', label='Search')

    class Meta:
        model = MedicalRecord
        fields = []  

    def filter_by_search(self, queryset, name, value):
        if value:
            query = Q()
            try:
                patient_id = int(value)
                query |= Q(patient__id=patient_id)  
            except ValueError:
                pass  
            
            query |= Q(patient__first_name__icontains=value)  
            query |= Q(patient__last_name__icontains=value)
            query |= Q(diagnosis__icontains=value)  
            
            queryset = queryset.filter(query)

        return queryset
