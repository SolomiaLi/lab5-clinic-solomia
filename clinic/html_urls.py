from django.urls import path
from clinic import html_views

urlpatterns = [
    # --- Patients HTML ---
    path('patients/', html_views.patient_list, name='patients-list'),  # Додав "s"
    path('patients/add/', html_views.patient_create, name='patient-add'),
    path('patients/<int:pk>/', html_views.patient_detail, name='patient-detail'),
    path('patients/<int:pk>/edit/', html_views.patient_edit, name='patient-edit'),
    path('patients/<int:pk>/delete/', html_views.patient_delete, name='patient-delete'),

    # --- Doctors HTML ---
    # Список - у множині (doctors-list), решта - в однині
    path('doctors/', html_views.doctor_list, name='doctors-list'),
    path('doctors/add/', html_views.doctor_create, name='doctor-add'),
    path('doctors/<int:pk>/', html_views.doctor_detail, name='doctor-detail'),
    path('doctors/<int:pk>/edit/', html_views.doctor_edit, name='doctor-edit'),
    path('doctors/<int:pk>/delete/', html_views.doctor_delete, name='doctor-delete'),

    # --- Medical Records HTML ---
    # --- Medical Records HTML ---
    # УВАГА: тут імена точно підлаштовані під твої помилки
    path('medical-records/', html_views.record_list, name='medical-records-list'),
    path('medical-records/add/', html_views.record_create, name='medical-record-add'),
    path('medical-records/<int:pk>/', html_views.record_detail, name='medical-record-detail'),
    path('medical-records/<int:pk>/edit/', html_views.record_edit, name='medical-record-edit'),
    path('medical-records/<int:pk>/delete/', html_views.record_delete, name='medical-record-delete'),
]