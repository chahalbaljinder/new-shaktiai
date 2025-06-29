"""
PostgreSQL Password Helper for SHAKTI-AI
This script helps you fix PostgreSQL authentication issues.
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_password(password):
    """Test a password with PostgreSQL."""
    try:
        conn_params = {
            'host': 'localhost',
            'user': 'postgres',
            'password': password,
            'port': '5432'
        }
        
        conn = psycopg2.connect(**conn_params)
        conn.close()
        return True
    except:
        return False

def try_common_passwords():
    """Try common PostgreSQL passwords."""
    common_passwords = [
        'postgres',
        'password',
        'admin',
        '123456',
        'root',
        '',  # empty password
        '8810',
        'shakti',
        'shakti123'
    ]
    
    print("🔍 Trying common PostgreSQL passwords...")
    
    for pwd in common_passwords:
        print(f"   Testing password: '{pwd}'", end="")
        if test_password(pwd):
            print(" ✅ SUCCESS!")
            return pwd
        else:
            print(" ❌")
    
    print("\n❌ None of the common passwords worked.")
    return None

def main():
    print("🛠️  PostgreSQL Password Helper")
    print("=" * 40)
    
    # Try current password from .env
    current_pwd = os.getenv('DB_PASSWORD', '8810')
    print(f"Testing current password from .env: '{current_pwd}'")
    
    if test_password(current_pwd):
        print("✅ Current password works! The issue might be elsewhere.")
        return
    else:
        print("❌ Current password doesn't work.")
    
    # Try common passwords
    working_password = try_common_passwords()
    
    if working_password is not None:
        print(f"\n🎉 Found working password: '{working_password}'")
        print("\n📝 Update your .env file:")
        print(f"DB_PASSWORD={working_password}")
        
        # Ask if user wants to update .env automatically
        update = input("\nDo you want me to update your .env file automatically? (y/n): ")
        if update.lower() == 'y':
            update_env_file(working_password)
    else:
        print("\n💡 Password not found. Here are your options:")
        print("\n1. RESET PostgreSQL PASSWORD:")
        print("   - Open Command Prompt as Administrator")
        print("   - Run: net stop postgresql-x64-17")
        print("   - Edit pg_hba.conf file (change 'md5' to 'trust')")
        print("   - Start PostgreSQL: net start postgresql-x64-17")
        print("   - Connect and change password: ALTER USER postgres PASSWORD 'newpassword';")
        print("   - Change pg_hba.conf back to 'md5'")
        print("   - Restart PostgreSQL")
        
        print("\n2. REINSTALL PostgreSQL:")
        print("   - Uninstall current PostgreSQL")
        print("   - Download fresh installer from postgresql.org")
        print("   - During installation, set a password you'll remember")
        
        print("\n3. USE pgAdmin:")
        print("   - Open pgAdmin")
        print("   - If you can connect, the password is working in pgAdmin")
        print("   - Check your connection settings")

def update_env_file(new_password):
    """Update the .env file with the correct password."""
    try:
        env_path = '.env'
        
        # Read current content
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update password line
        updated_lines = []
        for line in lines:
            if line.startswith('DB_PASSWORD='):
                updated_lines.append(f'DB_PASSWORD={new_password}\n')
            else:
                updated_lines.append(line)
        
        # Write back
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
        
        print(f"✅ Updated .env file with password: {new_password}")
        
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")

if __name__ == "__main__":
    main()
