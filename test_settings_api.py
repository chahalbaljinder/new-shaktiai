"""
Test Settings API Endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_get_profile():
    """Test GET profile endpoint"""
    print("\n🔍 Testing GET /api/settings/profile")
    response = requests.get(f"{BASE_URL}/api/settings/profile?user_id=3")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_update_profile():
    """Test PUT profile endpoint"""
    print("\n✏️ Testing PUT /api/settings/profile")
    data = {
        "user_id": 3,
        "name": "DRDO Admin Updated",
        "email": "admin@drdo.gov.in",
        "designation": "Senior Administrator",
        "establishment": "Delhi HQ"
    }
    response = requests.put(
        f"{BASE_URL}/api/settings/profile",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_notifications():
    """Test GET notifications endpoint"""
    print("\n🔔 Testing GET /api/settings/notifications")
    response = requests.get(f"{BASE_URL}/api/settings/notifications?user_id=3")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_update_notifications():
    """Test PUT notifications endpoint"""
    print("\n✏️ Testing PUT /api/settings/notifications")
    data = {
        "user_id": 3,
        "settings": {
            "expertResponses": True,
            "wishReminders": False,
            "weeklyCheckins": True,
            "communityUpdates": True,
            "emergencyAlerts": True,
            "voiceConfirmations": False
        }
    }
    response = requests.put(
        f"{BASE_URL}/api/settings/notifications",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_stats():
    """Test GET stats endpoint"""
    print("\n📊 Testing GET /api/settings/stats")
    response = requests.get(f"{BASE_URL}/api/settings/stats?user_id=3")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_export_data():
    """Test GET export endpoint"""
    print("\n💾 Testing GET /api/settings/export")
    response = requests.get(f"{BASE_URL}/api/settings/export?user_id=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response summary:")
    print(f"  - User: {data.get('user', {}).get('name')}")
    print(f"  - Wishes: {len(data.get('wishes', []))}")
    print(f"  - Feedback: {len(data.get('feedback', []))}")
    print(f"  - Queries: {len(data.get('knowledge_queries', []))}")
    print(f"  - Export Date: {data.get('export_date')}")

def test_password_change():
    """Test PUT password endpoint"""
    print("\n🔒 Testing PUT /api/settings/password (with wrong current password)")
    data = {
        "user_id": 3,
        "current_password": "wrong_password",
        "new_password": "new_secure_password"
    }
    response = requests.put(
        f"{BASE_URL}/api/settings/password",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING SETTINGS API ENDPOINTS")
    print("=" * 60)
    
    try:
        test_get_profile()
        test_update_profile()
        test_get_profile()  # Check if update worked
        test_get_notifications()
        test_update_notifications()
        test_get_stats()
        test_export_data()
        test_password_change()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
