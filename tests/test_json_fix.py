"""
Test and Fix Wishes Vault JSON Issue
"""

import json
from db_config import wishes_db

def test_wish_save_and_retrieve():
    """Test saving and retrieving wishes with JSON preferences."""
    
    # Test data
    user_id = "test_json_fix"
    content = "Test wish for JSON fix"
    sharing_preferences = {
        "auto_share": True,
        "preferred_method": "Email"
    }
    
    print("🧪 Testing wish save with JSON preferences...")
    
    try:
        # Save wish
        wish_id = wishes_db.save_wish(
            user_id=user_id,
            content=content,
            contact_name="Test Contact",
            contact_email="test@example.com",
            sharing_preferences=sharing_preferences
        )
        
        if wish_id:
            print(f"✅ Wish saved with ID: {wish_id}")
        else:
            print("❌ Failed to save wish")
            return False
        
        # Retrieve wishes
        print("🔍 Retrieving wishes...")
        wishes = wishes_db.get_wishes(user_id)
        
        if wishes:
            wish = wishes[0]
            print(f"✅ Retrieved wish: {wish['content']}")
            print(f"✅ Sharing preferences: {wish['sharing_preferences']}")
            print(f"✅ Type of preferences: {type(wish['sharing_preferences'])}")
        else:
            print("❌ No wishes retrieved")
            return False
        
        # Clean up
        wishes_db.delete_wish(wish_id, user_id)
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    print("🛠️  Testing JSON Fix for Wishes Vault")
    print("=" * 40)
    
    # Initialize database
    if wishes_db.init_database():
        print("✅ Database initialized")
    else:
        print("❌ Database initialization failed")
        exit(1)
    
    # Run test
    if test_wish_save_and_retrieve():
        print("\n🎉 JSON fix test PASSED!")
        print("✅ Wishes vault should now work correctly")
    else:
        print("\n❌ JSON fix test FAILED!")
        print("❌ There may still be an issue")
