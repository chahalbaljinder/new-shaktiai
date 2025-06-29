# 🌟 SHAKTI-AI: Advanced Emotional Support & Wellness Companion

> **A comprehensive AI-powered wellness platform with weather alerts, wishes vault, and intelligent emotional support**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

SHAKTI-AI is an advanced emotional support and wellness companion that combines AI-powered conversations, weather-based panic mode, secure wishes management, and comprehensive wellness resources. Built with modern technologies including PostgreSQL database integration and voice interaction capabilities.

## ✨ Key Features

### 🧠 **AI-Powered Emotional Support**
- Multi-agent AI system with specialized companions (Gynika, Maaya, Meher, Nyaya, Vaanya)
- Context-aware conversations with memory retention
- Personalized responses based on user interaction history
- Voice input and interactive communication

### 🌦️ **Weather-Based Panic Mode**
- Real-time weather monitoring and alerts
- Emergency contact integration during severe weather
- Air quality monitoring and health recommendations
- Compact, mobile-friendly weather dashboard

### 🔒 **Secure Wishes Vault**
- PostgreSQL-backed encrypted storage
- Contact management for trusted individuals
- Email and WhatsApp sharing capabilities
- Sharing history and preferences tracking
- Military-grade encryption (Fernet)

### 📚 **Knowledge Base Integration**
- Comprehensive wellness and mental health resources
- PDF document processing and vector search
- RAG (Retrieval Augmented Generation) capabilities
- Specialized knowledge bases for different AI companions

## 🏗️ Project Structure

```
shakti-ai/
├── 📱 app.py                      # Main Streamlit application
├── 📋 requirements.txt           # Python dependencies
├── 🔧 .env                       # Environment configuration
├── 📖 README.md                  # This file
│
├── 🧠 core/                      # Core AI functionality
│   ├── agents.py                 # AI agent definitions
│   ├── crew.py                   # CrewAI configuration
│   ├── llm.py                    # Language model setup
│   └── get_voice_input.py        # Voice input handling
│
├── 🗄️ database/                  # Database management
│   ├── db_config.py              # PostgreSQL configuration
│   ├── create_database.py        # Database setup script
│   ├── wishes_vault_db.py        # Wishes vault implementation
│   └── db_wishes.key             # Encryption key (auto-generated)
│
├── 📚 knowledge_base/            # AI knowledge resources
│   ├── document_processor.py     # PDF processing
│   ├── kb_manager.py             # Knowledge base management
│   ├── retriever.py              # Document retrieval
│   ├── vector_store.py           # Vector storage
│   ├── raw_pdfs/                 # Source documents
│   ├── processed/                # Processed vector stores
│   └── metadata/                 # Document metadata
│
├── 🧪 tests/                     # Test files
│   ├── test_db_connection.py     # Database connectivity tests
│   ├── test_complete_db.py       # Full database integration tests
│   ├── fix_postgres_password.py  # Password troubleshooting
│   └── test_*.py                 # Additional test files
│
├── 🛠️ utils/                     # Utility scripts
│   ├── setup_database.py         # GUI database setup
│   ├── quick_db_setup.py         # Quick setup script
│   └── setup_*.py                # Additional utilities
│
├── 📦 install/                   # Installation scripts
│   ├── install_and_setup.py      # Complete installation
│   ├── install_minimal.py        # Minimal installation
│   ├── install_windows.bat       # Windows batch installer
│   ├── install_windows.ps1       # PowerShell installer
│   └── install_unix.sh           # Unix/Linux installer
│
├── 📄 docs/                      # Documentation
│   ├── INSTALLATION_GUIDE.md     # Detailed installation guide
│   ├── POSTGRESQL_SETUP_COMPLETE.md  # Database setup guide
│   ├── FEATURE_ENHANCEMENTS_COMPLETED.md  # Development log
│   └── *.md                      # Additional documentation
│
├── 🗂️ legacy/                    # Legacy files
│   ├── wishes.enc                # Old encrypted wishes
│   └── wishes.key               # Old encryption key
│
└── 📊 logs/                      # Application logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd shakti-ai
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup PostgreSQL Database
```bash
# Run the database setup script
python utils/quick_db_setup.py

# Or setup manually:
createdb -U postgres shakti_ai_db
python database/create_database.py
```

### 4️⃣ Configure Environment
```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 5️⃣ Launch Application
```bash
streamlit run app.py
```

Visit `http://localhost:8501` to access SHAKTI-AI!

## 🔧 Configuration

### Environment Variables (.env)
```env
# Database Configuration
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# API Keys (Optional)
GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_weather_api_key

# Email Configuration (Optional)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

### Required APIs
- **Google Gemini API**: For AI conversations (free tier available)
- **OpenWeatherMap API**: For weather data (free tier available)

## 🎮 Usage Guide

### Main Interface
1. **Chat with AI**: Select an AI companion and start chatting
2. **Voice Input**: Click microphone icon for voice interaction
3. **Weather Mode**: Access panic mode for weather alerts
4. **Wishes Vault**: Store and manage personal wishes securely

### Weather Panic Mode
- Real-time weather monitoring
- Severe weather alerts
- Air quality information
- Emergency contact integration

### Wishes Vault
- Create encrypted personal wishes
- Add trusted contact information
- Share via email or WhatsApp
- View sharing history

## 🧪 Testing

### Database Tests
```bash
# Test database connection
python tests/test_db_connection.py

# Test complete database functionality
python tests/test_complete_db.py

# Fix password issues
python tests/fix_postgres_password.py
```

### Application Tests
```bash
# Test voice input
python tests/test_voice.py

# Test JSON handling
python tests/test_json_fix.py
```

## 🔒 Security Features

- **Encryption**: All wishes encrypted with Fernet (AES 128)
- **Database Security**: PostgreSQL with parameterized queries
- **Privacy**: No permanent storage of shared content
- **Access Control**: User-based data isolation
- **Secure Communication**: HTTPS recommended for production

## 🛠️ Development

### Adding New AI Agents
1. Define agent in `core/agents.py`
2. Add knowledge base in `knowledge_base/raw_pdfs/`
3. Process documents with `knowledge_base/document_processor.py`
4. Update crew configuration in `core/crew.py`

### Database Schema
- **wishes**: Encrypted wishes storage
- **sharing_history**: Sharing activity tracking
- **Indexes**: Optimized for user queries

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📊 Performance

- **Database**: PostgreSQL with optimized indexes
- **Caching**: Streamlit session state for UI performance
- **Vector Search**: FAISS for fast knowledge retrieval
- **Memory**: Efficient document processing pipeline

## 🆘 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql  # Linux
net start postgresql-x64-17       # Windows

# Test connection
python tests/test_db_connection.py
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Voice Input Issues**
```bash
# Install audio dependencies
pip install pyaudio speechrecognition
```

## 📈 Roadmap

- [ ] **User Authentication**: Multi-user support with authentication
- [ ] **Mobile App**: React Native companion app
- [ ] **Advanced Analytics**: User interaction insights
- [ ] **Cloud Deployment**: AWS/Azure deployment guides
- [ ] **API Integration**: RESTful API for third-party access
- [ ] **Multilingual Support**: Additional language support

## 🤝 Support

- **Documentation**: Check `docs/` folder for detailed guides
- **Issues**: Report bugs via GitHub issues
- **Community**: Join our Discord community
- **Email**: support@shakti-ai.com

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit**: Amazing web app framework
- **CrewAI**: Multi-agent AI framework
- **PostgreSQL**: Robust database system
- **Google Gemini**: Powerful language model
- **Open Source Community**: For endless inspiration

---

<div align="center">

**🌟 SHAKTI-AI: Empowering Wellness Through AI 🌟**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/your-repo)
[![Python](https://img.shields.io/badge/Built%20with-Python-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-red.svg)](https://streamlit.io/)

</div>
