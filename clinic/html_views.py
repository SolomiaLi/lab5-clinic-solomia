from django.shortcuts import render, redirect
# Імпортуємо твої обгортки репозиторіїв.
# Переконайся, що файл repository_wrapper.py існує там, де і був.
from .repository_wrapper import get_repos, commit, rollback

# -------------------- PATIENT --------------------
def patient_list(request):
    repos = get_repos()
    patients = repos.patients.all()
    return render(request, 'patients_list.html', {'patients': patients})

def patient_detail(request, pk):
    repos = get_repos()
    patient = repos.patients.get_by_id(pk)
    if not patient:
        return render(request, '404.html', status=404)
    return render(request, 'patient_detail.html', {'patient': patient})

def patient_create(request):
    if request.method == 'POST':
        repos = get_repos()
        try:
            repos.patients.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                date_of_birth=request.POST.get('date_of_birth'), # замість age
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                city=request.POST.get('city'),
                street=request.POST.get('street'),
                house_number=request.POST.get('house_number')
            )
            commit()
            return redirect('patient-list')
        except Exception as e:
            rollback()
            return render(request, 'patient_form.html', {'error': str(e)})
    return render(request, 'patient_form.html')

def patient_edit(request, pk):
    repos = get_repos()
    patient = repos.patients.get_by_id(pk)
    if request.method == 'POST':
        try:
            # ВИПРАВЛЕНО: Список полів для оновлення
            data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'date_of_birth': request.POST.get('date_of_birth'),
                'gender': request.POST.get('gender'),
                'phone': request.POST.get('phone'),
                'city': request.POST.get('city'),
                'street': request.POST.get('street'),
                'house_number': request.POST.get('house_number'),
            }
            # Оновлення через SQL (бо ORM немає методу update на об'єкті)
            with repos.conn.cursor() as cur:
                cols = ", ".join(f"{k} = %s" for k in data.keys())
                values = tuple(data.values()) + (pk,)
                cur.execute(f"UPDATE patients SET {cols} WHERE id = %s", values)
            commit()
            return redirect('patient-detail', pk=pk)
        except Exception as e:
            rollback()
            return render(request, 'patient_form.html', {'patient': patient, 'error': str(e)})
    return render(request, 'patient_form.html', {'patient': patient})

def patient_delete(request, pk):
    repos = get_repos()
    try:
        repos.patients.delete(pk)
        commit()
        return redirect('patient-list')
    except Exception as e:
        rollback()
        # Якщо помилка, повертаємося на деталі
        patient = repos.patients.get_by_id(pk)
        return render(request, 'patient_detail.html', {'patient': patient, 'error': str(e)})

# -------------------- DOCTOR --------------------
def doctor_list(request):
    repos = get_repos()
    doctors = repos.doctors.all()
    return render(request, 'doctors_list.html', {'doctors': doctors})

def doctor_detail(request, pk):
    repos = get_repos()
    doctor = repos.doctors.get_by_id(pk)
    if not doctor:
        return render(request, '404.html', status=404)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

def doctor_create(request):
    if request.method == 'POST':
        repos = get_repos()
        try:
            # ВИПРАВЛЕНО: Використовуємо phone_number замість specialty
            repos.doctors.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone_number=request.POST.get('phone_number') 
            )
            commit()
            return redirect('doctor-list')
        except Exception as e:
            rollback()
            return render(request, 'doctor_form.html', {'error': str(e)})
    return render(request, 'doctor_form.html')

def doctor_edit(request, pk):
    repos = get_repos()
    doctor = repos.doctors.get_by_id(pk)
    if request.method == 'POST':
        try:
            data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'phone_number': request.POST.get('phone_number')
            }
            with repos.conn.cursor() as cur:
                cols = ", ".join(f"{k} = %s" for k in data.keys())
                values = tuple(data.values()) + (pk,)
                cur.execute(f"UPDATE doctors SET {cols} WHERE id = %s", values)
            commit()
            return redirect('doctor-detail', pk=pk)
        except Exception as e:
            rollback()
            return render(request, 'doctor_form.html', {'doctor': doctor, 'error': str(e)})
    return render(request, 'doctor_form.html', {'doctor': doctor})

def doctor_delete(request, pk):
    repos = get_repos()
    try:
        repos.doctors.delete(pk)
        commit()
        return redirect('doctor-list')
    except Exception as e:
        rollback()
        doctor = repos.doctors.get_by_id(pk)
        return render(request, 'doctor_detail.html', {'doctor': doctor, 'error': str(e)})

# -------------------- MEDICAL RECORD --------------------
def record_list(request):
    repos = get_repos()
    records = repos.records.all()
    return render(request, 'medical_records_list.html', {'records': records})

def record_detail(request, pk):
    repos = get_repos()
    record = repos.records.get_by_id(pk)
    if not record:
        return render(request, '404.html', status=404)
    return render(request, 'medical_record_detail.html', {'record': record})

def record_create(request):
    if request.method == 'POST':
        repos = get_repos()
        try:
            repos.records.create(
                ID_patients=request.POST.get('ID_patients'),
                ID_disease=request.POST.get('ID_disease'),
                lab_test=request.POST.get('lab_test'),
                level_of_disease=request.POST.get('level_of_disease'),
                # Перевірка чекбокса: якщо є в POST - 1, інакше 0
                chronic=1 if 'chronic' in request.POST else 0
            )
            commit()
            return redirect('record-list')
        except Exception as e:
            rollback()
            return render(request, 'medical_record_form.html', {'error': str(e)})
    return render(request, 'medical_record_form.html')

def record_edit(request, pk):
    repos = get_repos()
    record = repos.records.get_by_id(pk)
    if request.method == 'POST':
        try:
            data = {
                'ID_patients': request.POST.get('ID_patients'),
                'ID_disease': request.POST.get('ID_disease'),
                'lab_test': request.POST.get('lab_test'),
                'level_of_disease': request.POST.get('level_of_disease'),
                'chronic': 1 if 'chronic' in request.POST else 0
            }
            with repos.conn.cursor() as cur:
                cols = ", ".join(f"{k} = %s" for k in data.keys())
                values = tuple(data.values()) + (pk,)
                cur.execute(f"UPDATE medical_records SET {cols} WHERE id = %s", values)
            commit()
            return redirect('record-detail', pk=pk)
        except Exception as e:
            rollback()
            return render(request, 'medical_record_form.html', {'record': record, 'error': str(e)})
    return render(request, 'medical_record_form.html', {'record': record})

def record_delete(request, pk):
    repos = get_repos()
    try:
        repos.records.delete(pk)
        commit()
        return redirect('record-list')
    except Exception as e:
        rollback()
        record = repos.records.get_by_id(pk)
        return render(request, 'medical_record_detail.html', {'record': record, 'error': str(e)})