from django.urls import path
from clinic import html_views

urlpatterns = [
    # --- Patients HTML ---
    path('patients/', html_views.patient_list, name='patient-list'),
    path('patients/add/', html_views.patient_create, name='patient-add'),
    path('patients/<int:pk>/', html_views.patient_detail, name='patient-detail'),
    path('patients/<int:pk>/edit/', html_views.patient_edit, name='patient-edit'),
    path('patients/<int:pk>/delete/', html_views.patient_delete, name='patient-delete'),

    # --- Doctors HTML ---
    path('doctors/', html_views.doctor_list, name='doctor-list'),
    path('doctors/add/', html_views.doctor_create, name='doctor-add'),
    path('doctors/<int:pk>/', html_views.doctor_detail, name='doctor-detail'),
    path('doctors/<int:pk>/edit/', html_views.doctor_edit, name='doctor-edit'),
    path('doctors/<int:pk>/delete/', html_views.doctor_delete, name='doctor-delete'),

    # --- Medical Records HTML ---
    path('medical-records/', html_views.record_list, name='record-list'),
    path('medical-records/add/', html_views.record_create, name='record-add'),
    path('medical-records/<int:pk>/', html_views.record_detail, name='record-detail'),
    path('medical-records/<int:pk>/edit/', html_views.record_edit, name='record-edit'),
    path('medical-records/<int:pk>/delete/', html_views.record_delete, name='record-delete'),
]