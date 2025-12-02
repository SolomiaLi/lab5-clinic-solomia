from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer, MedicalRecordSerializer, DoctorSerializer
from .repository_wrapper import get_repos, commit, rollback

# ---------------------- 1. CRUD для Patient ----------------------
class PatientsListCreate(APIView):

    def get(self, request):
        repos = get_repos()
        patients = repos.patients.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            repos = get_repos()
            try:
                new = repos.patients.create(**serializer.validated_data)
                commit()
                return Response(PatientSerializer(new).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                rollback()
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):

    def get(self, request, pk):
        repos = get_repos()
        p = repos.patients.get_by_id(pk)
        if not p:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(PatientSerializer(p).data)

    def put(self, request, pk):
        serializer = PatientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repos = get_repos()
        data = serializer.validated_data
        data.pop('id', None)
        if not data:
            return Response({"error": "No fields provided for update."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with repos.conn.cursor() as cur:
                cols = ", ".join(f"{k} = %s" for k in data.keys())
                values = tuple(data.values()) + (pk,)  # значення + id

                sql = f"UPDATE patients SET {cols} WHERE id = %s"
                cur.execute(sql, values)

            commit()
            updated = repos.patients.get_by_id(pk)
            if not updated:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(PatientSerializer(updated).data)
        except Exception as e:
            rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        repos = get_repos()
        try:
            ok = repos.patients.delete(pk)
            commit()
            if ok:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------- 2. Створення MedicalRecord ----------------------
class MedicalRecordCreate(APIView):

    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repos = get_repos()
        validated = serializer.validated_data

        try:
            create_kwargs = {}
            if 'ID_patients' in validated:
                create_kwargs['ID_patients'] = validated['ID_patients']
            if 'ID_disease' in validated:
                create_kwargs['ID_disease'] = validated['ID_disease']

            create_kwargs['lab_test'] = validated.get('lab_test')
            create_kwargs['level_of_disease'] = validated.get('level_of_disease')
            create_kwargs['chronic'] = 1 if validated.get('chronic') else 0

            new = repos.records.create(**create_kwargs)
            commit()
            return Response(MedicalRecordSerializer(new).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            rollback()
            return Response({'error': f"DB Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------- 3. Агрегований Звіт (за Patient ID) ----------------------
class PatientReport(APIView):

    def get(self, request, pk):
        repos = get_repos()
        patient = repos.patients.get_by_id(pk)
        if not patient:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            records = repos.records.for_patient(pk)
            total = len(records)
            chronic_count = sum(1 for r in records if getattr(r, 'chronic', False))
            unique_lab_tests = list(set(r.lab_test for r in records if r.lab_test))
            records_data = MedicalRecordSerializer(records, many=True).data

            report = {
                "patient_id": pk,
                "patient_name": f"{patient.first_name} {patient.last_name}",
                "total_records": total,
                "chronic_count": chronic_count,
                "unique_diseases": unique_lab_tests,
                "medical_records": records_data
            }
            return Response(report)
        except Exception as e:
            return Response({'error': f"Report Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------- 4. CRUD для Doctor ----------------------
class DoctorListCreate(APIView):

    def get(self, request):
        repos = get_repos()
        doctors = repos.doctors.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            repos = get_repos()
            try:
                new = repos.doctors.create(**serializer.validated_data)
                commit()
                return Response(DoctorSerializer(new).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                rollback()
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetail(APIView):

    def get(self, request, pk):
        repos = get_repos()
        d = repos.doctors.get_by_id(pk)
        if not d:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(DoctorSerializer(d).data)

    def put(self, request, pk):
        serializer = DoctorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repos = get_repos()
        data = serializer.validated_data
        data.pop('id', None)

        try:
            with repos.conn.cursor() as cur:
                cols = ", ".join(f"{k} = %s" for k in data.keys())
                values = tuple(data.values()) + (pk,)
                sql = f"UPDATE doctors SET {cols} WHERE id = %s"
                cur.execute(sql, values)

            commit()
            updated = repos.doctors.get_by_id(pk)
            if not updated:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(DoctorSerializer(updated).data)
        except Exception as e:
            rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        repos = get_repos()
        try:
            ok = repos.doctors.delete(pk)
            commit()
            if ok:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------- 5. CRUD для MedicalRecord ----------------------

class MedicalRecordListCreate(APIView):

    post = MedicalRecordCreate.post

    def get(self, request):
        repos = get_repos()
        records = repos.records.all()
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)


class MedicalRecordDetail(APIView):

    def get(self, request, pk):
        repos = get_repos()
        mr = repos.records.get_by_id(pk)
        if not mr:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(MedicalRecordSerializer(mr).data)

    def put(self, request, pk):
        serializer = MedicalRecordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repos = get_repos()
        validated = serializer.validated_data

        data_to_update = {}
        if 'ID_patients' in validated:
            data_to_update['ID_patients'] = validated['ID_patients']
        if 'ID_disease' in validated:
            data_to_update['ID_disease'] = validated['ID_disease']
        if 'lab_test' in validated:
            data_to_update['lab_test'] = validated['lab_test']
        if 'level_of_disease' in validated:
            data_to_update['level_of_disease'] = validated['level_of_disease']

        data_to_update['chronic'] = 1 if validated.get('chronic') else 0

        try:
            with repos.conn.cursor() as cur:
                cols = ", ".join(f"{k} = %s" for k in data_to_update.keys())
                values = tuple(data_to_update.values()) + (pk,)
                sql = f"UPDATE medical_records SET {cols} WHERE id = %s"
                cur.execute(sql, values)

            commit()
            updated = repos.records.get_by_id(pk)
            if not updated:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(MedicalRecordSerializer(updated).data)
        except Exception as e:
            rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        repos = get_repos()
        try:
            ok = repos.records.delete(pk)
            commit()
            if ok:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)