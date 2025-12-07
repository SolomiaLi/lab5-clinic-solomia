import requests

BASE_URL = "http://127.0.0.1:7777"

API_PREFIX = "/api"

AUTH = ("Solomia", "Q09liashchuk")

def print_response(resp):
    print(f"Status: {resp.status_code}")
    try:
        print("Body:", resp.json())
    except Exception:
        print("Text:", resp.text)
    print("-" * 40)


# 1. GET LIST
def get_clients_list():
    print("\n--- 1. ОТРИМАННЯ СПИСКУ (GET LIST) ---")
    url = f"{BASE_URL}{API_PREFIX}/clients/"
    resp = requests.get(url, auth=AUTH)
    print_response(resp)


# 2. CREATE
def create_client():
    print("\n--- 2. СТВОРЕННЯ (CREATE) ---")
    url = f"{BASE_URL}{API_PREFIX}/clients/"
    data = {
        "first_name": "TestBot",
        "last_name": "API_User",
        "email": "bot@test.com",
        "phone": "+380991234567"
    }

    resp = requests.post(url, json=data, auth=AUTH)
    print_response(resp)

    if resp.status_code in [200, 201]:
        return resp.json().get('id')
    return None


# 3. GET BY ID
def get_client_by_id(client_id):
    print(f"\n--- 3. ОТРИМАННЯ ПО ID (GET ID={client_id}) ---")
    url = f"{BASE_URL}{API_PREFIX}/clients/{client_id}/"
    resp = requests.get(url, auth=AUTH)
    print_response(resp)


# 4. UPDATE
def update_client(client_id):
    print(f"\n--- 4. ОНОВЛЕННЯ (UPDATE ID={client_id}) ---")
    url = f"{BASE_URL}{API_PREFIX}/clients/{client_id}/"

    data = {
        "first_name": "UpdatedName",
        "last_name": "UpdatedSurname",
        "phone": "+380000000000",
        "email": "update@test.com"
    }

    resp = requests.put(url, json=data, auth=AUTH)
    print_response(resp)


# 5. DELETE
def delete_client(client_id):
    print(f"\n--- 5. ВИДАЛЕННЯ (DELETE ID={client_id}) ---")
    url = f"{BASE_URL}{API_PREFIX}/clients/{client_id}/"
    resp = requests.delete(url, auth=AUTH)

    print(f"Status: {resp.status_code}")
    if resp.status_code == 204:
        print("Успішно видалено!")
    else:
        print("Щось пішло не так при видаленні")
    print("-" * 40)


if __name__ == "__main__":
    get_clients_list()
    new_id = create_client()

    if new_id:
        get_client_by_id(new_id)
        update_client(new_id)
        delete_client(new_id)
        get_clients_list()
    else:
        print("Не вдалося створити клієнта, зупиняємо тест.")