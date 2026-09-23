import requests


BASE_URL = "http://127.0.0.1:5000/api"


def check(condition, message):
    """Jednoduchy assert s citelnym vystupem."""
    assert condition, f"CHYBA: {message}"
    print(f"OK: {message}")


print("1. HEALTH CHECK")
response = requests.get(f"{BASE_URL}/health", timeout=5)
print("Status:", response.status_code)
print("Response:", response.json())
check(response.status_code == 200, "API vraci status 200")
check(response.json()["status"] == "ok", "API hlasi stav ok")


print("\n2. POST - VYTVORENI POLITIKY")
payload = {
    "name": "Block USB copy",
    "action": "block",
    "enabled": True,
}
response = requests.post(f"{BASE_URL}/policies", json=payload, timeout=5)
print("Request:", payload)
print("Status:", response.status_code)
print("Response:", response.json())
check(response.status_code == 201, "nova politika vraci status 201")
check(response.json()["name"] == payload["name"], "response obsahuje spravny nazev")
check(response.json()["action"] == "block", "response obsahuje spravnou akci")
policy_id = response.json()["id"]


print("\n3. GET - NACTENI POLITIKY")
response = requests.get(f"{BASE_URL}/policies/{policy_id}", timeout=5)
print("Status:", response.status_code)
print("Response:", response.json())
check(response.status_code == 200, "existujici politika vraci status 200")
check(response.json()["id"] == policy_id, "API vratilo spravne ID")


print("\n4. NEGATIVNI TEST - CHYBI POVINNE POLE NAME")
invalid_payload = {"action": "block"}
response = requests.post(f"{BASE_URL}/policies", json=invalid_payload, timeout=5)
print("Status:", response.status_code)
print("Response:", response.json())
check(response.status_code == 400, "nevalidni request vraci status 400")
check("error" in response.json(), "chybova response obsahuje popis chyby")


print("\n5. PATCH - VYPNUTI POLITIKY")
response = requests.patch(
    f"{BASE_URL}/policies/{policy_id}",
    json={"enabled": False},
    timeout=5,
)
print("Status:", response.status_code)
print("Response:", response.json())
check(response.status_code == 200, "uprava politiky vraci status 200")
check(response.json()["enabled"] is False, "politika je vypnuta")


print("\n6. DELETE - SMAZANI POLITIKY")
response = requests.delete(f"{BASE_URL}/policies/{policy_id}", timeout=5)
print("Status:", response.status_code)
check(response.status_code == 204, "smazani vraci status 204")


print("\n7. OVERENI SMAZANI")
response = requests.get(f"{BASE_URL}/policies/{policy_id}", timeout=5)
print("Status:", response.status_code)
print("Response:", response.json())
check(response.status_code == 404, "smazana politika uz neexistuje")


print("\nVSECHNY TESTY PROSLY.")
