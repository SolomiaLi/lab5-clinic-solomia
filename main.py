import pymysql
from repository import RepositoryManager, PatientRepository, DoctorRepository, MedicalRecordRepository
from entities import Patient, Doctor, MedicalRecord

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Q09liashchuk',
    'database': 'mydb',
    'cursorclass': pymysql.cursors.DictCursor
}

def demo(repos: RepositoryManager):
    print("=== Demo repository pattern (MySQL) ===")

    p = repos.patients.create(first_name="Світлана", last_name="Олійник", date_of_birth="1983-03-12", gender="Жіноча",
                              phone="380507845", city="Тернопіль", street="Проспект Перемоги", house_number=76)
    print("Created patient:", p)

    d = repos.doctors.create(first_name="Дмитро", last_name="Марчук", phone_number="677694999")
    print("Created doctor:", d)

    mr = repos.records.create(ID_patients=p.id, ID_disease=301, lab_test="CBC", level_of_disease=1,
                              chronic=0)
    print("Created medical record:", mr)

    all_patients = repos.patients.all()
    print("\nAll patients:")
    for x in all_patients:
        print(" ", x)

    found = repos.patients.get_by_id(p.id)
    print("\nFound by id:", found)

    recs = repos.records.for_patient(p.id)
    print("\nRecords for patient", p.id)
    for r in recs:
        print(" ", r)

    recs = repos.records.for_patient(p.id)
    for r in recs:
        repos.records.delete(r.id)
    print(f"\nDeleted {len(recs)} medical record(s) for patient {p.id}")

    deleted = repos.patients.delete(p.id)
    if deleted:
        print(f"\nPatient with id={p.id} was successfully deleted.")
    else:
        print(f"\nFailed to delete patient with id={p.id}.")

    print("\nCheck after deletion:")
    still_exists = repos.patients.get_by_id(p.id)
    print("Found:", still_exists)

if __name__ == "__main__":
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        repos = RepositoryManager(conn)
        demo(repos)
        conn.commit()
        print("\n--- Дані успішно зафіксовані в MySQL ---")

    except Exception as e:
        print(f"\nПОМИЛКА: Не вдалося підключитися або виконати запит. Перевірте PyMySQL і {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

