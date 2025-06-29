"""
PostgreSQL Database Setup for SHAKTI-AI
This script helps set up the PostgreSQL database and environment variables.
"""

import os
import streamlit as st
import psycopg2
from db_config import DB_CONFIG, wishes_db

def show_database_setup():
    """Show database setup interface in Streamlit."""
    st.markdown("### 🛠️ Database Setup")
    
    st.info("""
    **PostgreSQL Configuration Required**
    
    SHAKTI-AI now uses PostgreSQL for secure wishes storage. Please ensure:
    1. PostgreSQL is installed and running
    2. Database credentials are configured
    3. Database connection is successful
    """)
    
    with st.expander("📋 Database Configuration", expanded=True):
        st.markdown("**Current Configuration:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.code(f"Host: {DB_CONFIG['host']}")
            st.code(f"Database: {DB_CONFIG['database']}")
            st.code(f"User: {DB_CONFIG['user']}")
        with col2:
            st.code(f"Port: {DB_CONFIG['port']}")
            st.code(f"Password: {'*' * len(DB_CONFIG['password'])}")
        
        st.markdown("**Environment Variables:**")
        st.code("""
# Add these to your .env file or system environment:
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
        """)
    
    with st.expander("🔧 Test Database Connection"):
        if st.button("Test Connection", use_container_width=True):
            test_database_connection()
    
    with st.expander("🚀 Initialize Database"):
        st.warning("⚠️ This will create the required tables for the wishes vault.")
        if st.button("Initialize Database Tables", use_container_width=True):
            initialize_database()

def test_database_connection():
    """Test the database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        st.success("✅ Database connection successful!")
        st.info(f"PostgreSQL Version: {version}")
        return True
        
    except psycopg2.OperationalError as e:
        st.error(f"❌ Database connection failed: {e}")
        st.markdown("""
        **Common solutions:**
        1. Check if PostgreSQL is running
        2. Verify database credentials
        3. Ensure database exists
        4. Check firewall/network settings
        """)
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return False

def initialize_database():
    """Initialize the database tables."""
    try:
        if wishes_db.init_database():
            st.success("✅ Database tables initialized successfully!")
            st.info("The wishes vault is now ready to use with PostgreSQL backend.")
        else:
            st.error("❌ Failed to initialize database tables.")
    except Exception as e:
        st.error(f"❌ Database initialization error: {e}")

def create_env_file():
    """Create a sample .env file with database configuration."""
    env_content = """# SHAKTI-AI Database Configuration
# PostgreSQL Database Settings
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_PORT=5432

# Email Configuration (optional)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Other configurations
DEBUG=False
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file_path):
        try:
            with open(env_file_path, 'w') as f:
                f.write(env_content)
            st.success(f"✅ Created .env file at: {env_file_path}")
            st.info("Please edit the .env file with your actual database credentials.")
        except Exception as e:
            st.error(f"❌ Failed to create .env file: {e}")
    else:
        st.info("📁 .env file already exists.")

def show_installation_guide():
    """Show PostgreSQL installation guide."""
    st.markdown("### 📖 PostgreSQL Installation Guide")
    
    tab1, tab2, tab3 = st.tabs(["Windows", "macOS", "Linux"])
    
    with tab1:
        st.markdown("""
        **Windows Installation:**
        
        1. **Download PostgreSQL:**
           - Visit https://www.postgresql.org/download/windows/
           - Download the Windows installer
        
        2. **Install PostgreSQL:**
           - Run the installer as administrator
           - Follow the setup wizard
           - Remember the password you set for the 'postgres' user
        
        3. **Verify Installation:**
           ```cmd
           psql --version
           ```
        
        4. **Create Database:**
           ```sql
           createdb -U postgres shakti_ai_db
           ```
        """)
    
    with tab2:
        st.markdown("""
        **macOS Installation:**
        
        1. **Using Homebrew (Recommended):**
           ```bash
           brew install postgresql
           brew services start postgresql
           ```
        
        2. **Create Database:**
           ```bash
           createdb shakti_ai_db
           ```
        
        3. **Alternative - PostgreSQL.app:**
           - Download from https://postgresapp.com/
           - Drag to Applications folder
           - Start the app
        """)
    
    with tab3:
        st.markdown("""
        **Linux Installation:**
        
        1. **Ubuntu/Debian:**
           ```bash
           sudo apt update
           sudo apt install postgresql postgresql-contrib
           sudo systemctl start postgresql
           sudo systemctl enable postgresql
           ```
        
        2. **CentOS/RHEL:**
           ```bash
           sudo yum install postgresql-server postgresql-contrib
           sudo postgresql-setup initdb
           sudo systemctl start postgresql
           sudo systemctl enable postgresql
           ```
        
        3. **Create Database:**
           ```bash
           sudo -u postgres createdb shakti_ai_db
           ```
        """)

if __name__ == "__main__":
    st.set_page_config(
        page_title="SHAKTI-AI Database Setup",
        page_icon="🛠️",
        layout="wide"
    )
    
    st.title("🛠️ SHAKTI-AI Database Setup")
    
    tab1, tab2, tab3 = st.tabs(["Database Setup", "Installation Guide", "Environment Setup"])
    
    with tab1:
        show_database_setup()
    
    with tab2:
        show_installation_guide()
    
    with tab3:
        st.markdown("### 🔧 Environment Setup")
        if st.button("Create Sample .env File", use_container_width=True):
            create_env_file()
        
        st.markdown("### 📝 Required Python Packages")
        st.code("""
pip install psycopg2-binary python-dotenv
        """)
        
        st.markdown("### 🔐 Security Notes")
        st.info("""
        - Never commit your .env file to version control
        - Use strong passwords for database access
        - Consider using connection pooling for production
        - Regular backups are recommended
        """)
