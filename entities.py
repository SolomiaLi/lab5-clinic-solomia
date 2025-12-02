class Patient:
    def __init__(self, id, first_name, last_name, date_of_birth=None, gender=None, phone=None, city=None, street=None, house_number=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.city = city
        self.street = street
        self.house_number = house_number

    def __repr__(self):
        return f"Patient(id={self.id}, name='{self.first_name} {self.last_name}', city='{self.city}')"


class Doctor:
    def __init__(self, id, first_name, last_name, phone_number=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __repr__(self):
        return f"Doctor(id={self.id}, name='Dr. {self.first_name} {self.last_name}')"


class MedicalRecord:
    def __init__(self, id, ID_patients, ID_disease=None, lab_test=None, level_of_disease=None, chronic=False):
        self.id = id
        self.ID_patients = ID_patients
        self.ID_disease = ID_disease
        self.lab_test = lab_test
        self.level_of_disease = level_of_disease
        self.chronic = bool(chronic)

    def __repr__(self):
        return (f"MedicalRecord(id={self.id}, patient_id={self.ID_patients} "
                f"disease='{self.ID_disease}', chronic={self.chronic})")
