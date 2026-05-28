import requests

BASE_URL = "http://127.0.0.1:8000"


def register_user(data):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def login_user(data):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
def admin_login(data):
    try:
        response = requests.post(f"{BASE_URL}/auth/admin/login", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
def predict_heart(data, token=None):
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.post(
            f"{BASE_URL}/predict/heart",
            json=data,
            headers=headers
        )
        return response.json()

    except Exception as e:
        return {"error": str(e)}
    
def predict_fitness(data, token=None):
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.post(
            f"{BASE_URL}/predict/fitness",
            json=data,
            headers=headers
        )

        # 🔴 HANDLE EMPTY RESPONSE
        if response.status_code != 200:
            return {"error": response.text}

        return response.json()

    except Exception as e:
        return {"error": str(e)}
    
def get_dashboard(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(f"{BASE_URL}/dashboard", headers=headers)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
    
def get_admin_dashboard(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/admin/dashboard", headers=headers).json()


def get_all_heart(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/admin/heart", headers=headers).json()


def get_all_fitness(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/admin/fitness", headers=headers).json()

def send_feedback(data, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(
            f"{BASE_URL}/feedback",
            json=data,
            headers=headers
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}
    
def get_all_feedback(token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{BASE_URL}/admin/feedback",
            headers=headers
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}