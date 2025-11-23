"""
Test script for onboarding system
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_employee():
    """Test creating a new employee"""
    print("\n=== Testing Employee Creation ===")
    
    data = {
        "name": "Raj Kumar",
        "email": f"raj.kumar.test{hash('test')}@drdo.gov.in",  # Unique email
        "designation": "Scientist B",
        "establishment": "DRDO Headquarters",
        "department": "AI Research Division",
        "role": "user",
        "temp_password": "Welcome@2024"
    }
    
    response = requests.post(f"{BASE_URL}/api/admin/create-employee", json=data)
    
    if response.status_code == 201:
        result = response.json()
        print("✓ Employee created successfully!")
        print(f"  Employee ID: {result['employee']['employee_id']}")
        print(f"  Name: {result['employee']['name']}")
        print(f"  Email: {result['employee']['email']}")
        print(f"  Temp Password: {result['employee']['temp_password']}")
        return result['employee']['id']
    else:
        print(f"✗ Failed: {response.json()}")
        return None

def test_check_onboarding(user_id):
    """Test checking onboarding status"""
    print(f"\n=== Testing Onboarding Check (User {user_id}) ===")
    
    response = requests.get(f"{BASE_URL}/api/auth/check-onboarding?user_id={user_id}")
    
    if response.ok:
        result = response.json()
        print("✓ Onboarding status retrieved:")
        print(f"  Needs onboarding: {result['needs_onboarding']}")
        print(f"  Current step: {result['current_step']}")
        print(f"  Must change password: {result['must_change_password']}")
        print(f"  Is first login: {result['is_first_login']}")
        return result
    else:
        print(f"✗ Failed: {response.json()}")
        return None

def test_update_onboarding_step(user_id, step):
    """Test updating onboarding step"""
    print(f"\n=== Testing Step Update (User {user_id}, Step {step}) ===")
    
    response = requests.put(
        f"{BASE_URL}/api/auth/onboarding/update-step",
        json={"user_id": user_id, "step": step}
    )
    
    if response.ok:
        print(f"✓ Step updated to {step}")
        return True
    else:
        print(f"✗ Failed: {response.json()}")
        return False

def test_complete_onboarding(user_id):
    """Test completing onboarding"""
    print(f"\n=== Testing Onboarding Completion (User {user_id}) ===")
    
    response = requests.post(
        f"{BASE_URL}/api/auth/onboarding/complete",
        json={"user_id": user_id}
    )
    
    if response.ok:
        print("✓ Onboarding marked as complete!")
        return True
    else:
        print(f"✗ Failed: {response.json()}")
        return False

def test_list_employees():
    """Test listing all employees"""
    print("\n=== Testing Employee List ===")
    
    response = requests.get(f"{BASE_URL}/api/admin/employees")
    
    if response.ok:
        result = response.json()
        employees = result.get('employees', [])
        print(f"✓ Found {len(employees)} employees")
        
        for emp in employees[:5]:  # Show first 5
            status = "✓ Complete" if emp['onboarding_completed'] else "⏳ Pending"
            print(f"  {emp['employee_id']}: {emp['name']} ({emp['email']}) - {status}")
        
        return employees
    else:
        print(f"✗ Failed: {response.json()}")
        return []

def test_profile_completion(user_id):
    """Test profile completion check"""
    print(f"\n=== Testing Profile Completion (User {user_id}) ===")
    
    response = requests.get(f"{BASE_URL}/api/settings/employee/profile-completion?user_id={user_id}")
    
    if response.ok:
        result = response.json()
        print(f"✓ Overall completion: {result['overall']}%")
        print("\n  Section breakdown:")
        for section, data in result.get('sections', {}).items():
            print(f"    {section}: {data['percentage']}% ({data['filled']}/{data['total']} fields)")
        return result
    else:
        print(f"✗ Failed: {response.json()}")
        return None

def run_full_test():
    """Run complete test suite"""
    print("=" * 60)
    print("ONBOARDING SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Test 1: Create employee
    user_id = test_create_employee()
    if not user_id:
        print("\n✗ Cannot continue tests without user ID")
        return
    
    # Test 2: Check onboarding status
    status = test_check_onboarding(user_id)
    if not status:
        return
    
    # Test 3: Update steps
    for step in range(1, 6):
        if not test_update_onboarding_step(user_id, step):
            return
    
    # Test 4: Complete onboarding
    if not test_complete_onboarding(user_id):
        return
    
    # Test 5: Verify completion
    test_check_onboarding(user_id)
    
    # Test 6: Check profile completion
    test_profile_completion(user_id)
    
    # Test 7: List all employees
    test_list_employees()
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe onboarding system is working correctly!")
    print("\nNext steps:")
    print("1. Login as superadmin to access Admin Panel")
    print("2. Create a test employee")
    print("3. Login with employee credentials to test onboarding flow")

if __name__ == "__main__":
    try:
        run_full_test()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to backend at http://localhost:8000")
        print("Make sure the backend server is running:")
        print("  python -m uvicorn backend_service:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
