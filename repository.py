import pymysql
from pymysql.connections import Connection as MySQLConnection
from typing import List, Optional, Callable
from entities import Patient, Doctor, MedicalRecord

class BaseRepository:
    def __init__(self, connection: MySQLConnection, table_name: str, mapper: Callable):

        self.conn = connection
        self.table = table_name
        self.mapper = mapper

    def all(self) -> List:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table}")
            rows = cur.fetchall()
            return [self.mapper(row) for row in rows]

    def get_by_id(self, id: int) -> Optional:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table} WHERE id = %s", (id,))
            row = cur.fetchone()
            if row:
                return self.mapper(row)
            return None

    def create(self, **kwargs):
        with self.conn.cursor() as cur:
            cols = ", ".join(kwargs.keys())
            placeholders = ", ".join("%s" for _ in kwargs)
            values = tuple(kwargs.values())
            sql = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
            cur.execute(sql, values)
            new_id = cur.lastrowid
            return self.get_by_id(new_id)

    def delete(self, id: int) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table} WHERE id = %s", (id,))
            return cur.rowcount > 0

class PatientRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, "patients", self._map_row)

    @staticmethod
    def _map_row(row):
        return Patient(id=row['id'], first_name=row['first_name'], last_name=row['last_name'],
                       date_of_birth=row['date_of_birth'], gender=row['gender'],
                       phone=row['phone'], city=row['city'], street=row['street'], house_number=row['house_number'])


class DoctorRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, "doctors", self._map_row)

    @staticmethod
    def _map_row(row):
        return Doctor(id=row['id'], first_name=row['first_name'], last_name=row['last_name'],
                      phone_number=row['phone_number'])


class MedicalRecordRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, "medical_records", self._map_row)

    @staticmethod
    def _map_row(row):
        return MedicalRecord(id=row['id'], ID_patients=row['ID_patients'],
                             ID_disease=str(row['ID_disease']), lab_test=row['lab_test'],
                             level_of_disease=row['level_of_disease'], chronic=row['chronic'])

    def for_patient(self, patient_id: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM medical_records WHERE ID_patients = %s", (patient_id,))
            rows = cur.fetchall()
            return [self._map_row(r) for r in rows]


class RepositoryManager:
    def __init__(self, connection: MySQLConnection):
        self.conn = connection
        self._patient_repo = None
        self._doctor_repo = None
        self._record_repo = None

    @property
    def patients(self) -> PatientRepository:
        if self._patient_repo is None:
            self._patient_repo = PatientRepository(self.conn)
        return self._patient_repo

    @property
    def doctors(self) -> DoctorRepository:
        if self._doctor_repo is None:
            self._doctor_repo = DoctorRepository(self.conn)
        return self._doctor_repo

    @property
    def records(self) -> MedicalRecordRepository:
        if self._record_repo is None:
            self._record_repo = MedicalRecordRepository(self.conn)
        return self._record_repo
