from django.urls import path
from .views import PatientsListCreate, PatientDetail, PatientReport, MedicalRecordCreate, DoctorListCreate, \
    MedicalRecordListCreate, MedicalRecordDetail, DoctorDetail
from django.urls import path, include

urlpatterns = [
    path('patients/', PatientsListCreate.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', PatientDetail.as_view(), name='patient-detail'),

    path('patients/<int:pk>/report/', PatientReport.as_view(), name='patient-report'),

    path('medical-records/', MedicalRecordCreate.as_view(), name='medical-record-create'),

    path('doctors/', DoctorListCreate.as_view(), name='doctors-list-create'),
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),

    path('medical-records/', MedicalRecordListCreate.as_view(), name='medical-records-list-create'),
    path('medical-records/<int:pk>/', MedicalRecordDetail.as_view(), name='medical-record-detail'),
]
