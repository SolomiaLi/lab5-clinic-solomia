from entities import Patient, Doctor, MedicalRecord
from rest_framework import serializers

class PatientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    street = serializers.CharField(max_length=200)
    house_number = serializers.CharField(max_length=50)

class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(required=False, allow_null=True)

class MedicalRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ID_patients = serializers.IntegerField()
    ID_disease = serializers.IntegerField(required=False, allow_null=True)
    lab_test = serializers.CharField(required=False, allow_null=True)
    level_of_disease = serializers.IntegerField(required=False, allow_null=True)
    chronic = serializers.BooleanField(default=False)
