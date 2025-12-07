import requests

BASE_URL = "http://127.0.0.1:8000/api"   # твій сервер


def print_response(title, resp):
    print("=" * 40)
    print(title)
    print("Status:", resp.status_code)
    try:
        print("JSON:", resp.json())
    except Exception:
        print("Text:", resp.text)


def get_patients_list():
    url = f"{BASE_URL}/patients/"
    resp = requests.get(url)
    print_response("GET patients list", resp)


def get_patient_by_id(patient_id: int):
    url = f"{BASE_URL}/patients/{patient_id}/"
    resp = requests.get(url)
    print_response(f"GET patient id={patient_id}", resp)


def create_patient():
    url = f"{BASE_URL}/patients/"
    data = {
        "first_name": "ApiClient",
        "last_name": "Test",
        "date_of_birth": "1995-04-12",   # формат YYYY-MM-DD
        "gender": "Чоловіча",
        "phone": "501234512",
        "city": "Київ",
        "street": "Хрещатик",
        "house_number": "10",
    }
    resp = requests.post(url, json=data)
    print_response("CREATE patient", resp)
    if resp.status_code in (200, 201):
        try:
            return resp.json().get("id")
        except Exception:
            return None
    return None


def update_patient(patient_id: int):
    url = f"{BASE_URL}/patients/{patient_id}/"
    data = {
        "first_name": "ApiClientUpdated",
        "last_name": "User",
        "date_of_birth": "1990-01-01",
        "gender": "Жіноча",
        "phone": "507778899",
        "city": "Львів",
        "street": "Зелена",
        "house_number": "20",
    }
    resp = requests.put(url, json=data)
    print_response(f"UPDATE patient id={patient_id}", resp)


def delete_patient(patient_id: int):
    url = f"{BASE_URL}/patients/{patient_id}/"
    resp = requests.delete(url)
    print_response(f"DELETE patient id={patient_id}", resp)


if __name__ == "__main__":
    # 1. список до змін
    get_patients_list()

    # 2. створити пацієнта
    new_id = create_patient()

    if new_id:
        # 3. отримати по id
        get_patient_by_id(new_id)

        # 4. оновити
        update_patient(new_id)

        # 5. видалити
        delete_patient(new_id)

    # 6. список після всіх операцій
    get_patients_list()
