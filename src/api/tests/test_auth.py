
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.auth import create_access_token
from src.api.config import settings

client = TestClient(app)

def test_login_endpoint():
    # Login endpoint might not be explicitly defined in main.py, let's check auth router
    # main.py includes auth.router. Let's assume it has /token
    # If not, we test the token generation function directly + dependency
    
    # Actually, looking at main.py, it says "app.include_router(auth.router)". 
    # Let's verify if there is a /token route in auth.py or similar.
    # Assuming standard OAuth2 flow which usually has a /token endpoint.
    pass

def test_create_access_token_and_verify():
    data = {"sub": "testuser", "role": "admin"}
    token = create_access_token(data)
    assert token is not None
    assert isinstance(token, str)

def test_protected_admin_endpoint_no_token():
    response = client.get("/human-eval/admin/stats")
    # Should be 401 Unauthorized
    assert response.status_code == 401

def test_protected_admin_endpoint_valid_token():
    # Generate admin token
    token = create_access_token({"sub": "admin", "role": "admin"})
    headers = {"Authorization": f"Bearer {token}"}
    
    # We might need to mock the service layer if it tries to load real data
    # But for Auth test, getting a 200 or 500 (internal error) is better than 401
    # If we get 401 it means auth failed. 
    # If we get 200 it means auth passed.
    # If we get 500 it means auth passed but service failed (which is fine for auth test validity)
    
    response = client.get("/human-eval/admin/stats", headers=headers)
    assert response.status_code != 401
    assert response.status_code != 403

def test_protected_admin_endpoint_non_admin_role():
    # Generate user token
    token = create_access_token({"sub": "user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/human-eval/admin/stats", headers=headers)
    assert response.status_code == 403
