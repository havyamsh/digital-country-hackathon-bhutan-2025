# Sovereign AI Bhutan 🏔️

A comprehensive AI assistant system built specifically for Bhutan, supporting both English and Dzongkha languages. This system provides government services assistance, legal guidance, cultural information, and tourism support while preserving Bhutanese values and promoting Gross National Happiness.

## 🎯 Features

### Core Capabilities
- **Multilingual Support**: English and Dzongkha (རྫོང་ཁ)
- **Specialized AI Agents**: 
  - Civil Service Assistant (གཞུང་འབྲེལ་ལས་ཀའི་རོགས་རམ།)
  - Tax & Finance Assistant (ཁྲལ་དང་དངུལ་གྱི་རོགས་རམ།)
  - Constitution & Law Guide (རྩ་ཁྲིམས་དང་ཁྲིམས་ལུགས།)
  - Tourism & Culture Guide (འགྲུལ་བསྐྱོད་དང་རིག་གཞུང་།)

### Technical Features
- **Modern Web Interface**: Responsive design with beautiful UI/UX
- **AI-Powered Backend**: Flask + Ollama integration
- **Knowledge Base**: Comprehensive Bhutanese government and cultural data
- **Real-time Chat**: Interactive conversation interface
- **Cultural Sensitivity**: Built-in respect for Bhutanese values and customs
- **Offline Capability**: Service worker for basic offline functionality

## 🏗️ Architecture

```
sovereign-ai-bhutan/
├── app.py                          # Flask main application
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Main HTML template
├── static/
│   ├── css/
│   │   └── styles.css            # Comprehensive styling
│   └── js/
│       ├── script.js             # Frontend JavaScript
│       └── sw.js                 # Service Worker
├── models/
│   └── ollama_client.py          # Ollama integration
├── agents/
│   ├── civil_service_agent.py    # Government services
│   ├── tax_agent.py              # Tax and finance
│   ├── constitution_agent.py     # Legal and constitutional
│   └── tourism_agent.py          # Tourism and culture
├── utils/
│   ├── language_utils.py         # Dzongkha translation utilities
│   └── knowledge_base.py         # Data management
└── data/
    ├── civil_service.json        # Government service data
    ├── tax.json                  # Tax information
    ├── constitution.json         # Constitutional data
    └── tourism.json              # Tourism and cultural data
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Ollama (for AI model serving)
- Modern web browser

### Step 1: Install Ollama
```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models
ollama pull gemma:2b
ollama pull mistral:7b
```

### Step 2: Clone and Setup Application
```bash
# Clone the repository
git clone <repository-url>
cd sovereign-ai-bhutan

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Start Services
```bash
# Start Ollama service (in separate terminal)
ollama serve

# Start Flask application
python app.py
```

### Step 4: Access Application
Open your browser and navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables
Create a `.env` file for custom configuration:
```env
FLASK_ENV=development
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=gemma:2b
LOG_LEVEL=INFO
```

### Model Configuration
Edit `models/ollama_client.py` to change default models:
```python
self.available_models = ["gemma:2b", "mistral:7b", "llama3:8b"]
self.current_model = "gemma:2b"  # Change default model
```

## 📊 Usage

### Basic Chat
1. Open the application in your browser
2. Select preferred language (English/Dzongkha)
3. Choose an AI assistant or use general chat
4. Type your question and press Enter

### Specialized Assistance
- **Government Services**: Ask about job applications, documentation, civil procedures
- **Tax Information**: Get help with tax rates, filing requirements, business registration
- **Legal Guidance**: Understand constitutional rights, legal procedures, court system
- **Tourism & Culture**: Learn about attractions, festivals, cultural etiquette

### Language Support
- Switch between English and Dzongkha using the language selector
- The system automatically handles basic translation for common terms
- Cultural context is preserved in both languages

## 🧠 AI Models

### Supported Models
- **Gemma 2B**: Fast, efficient for general queries
- **Mistral 7B**: Better reasoning for complex questions
- **LLaMA 3 8B**: Advanced capabilities for detailed responses

### Model Selection
The system automatically selects the best model based on query complexity. You can manually switch models by modifying the `current_model` property in the Ollama client.

## 📚 Knowledge Base

### Data Sources
- Bhutanese Constitution and laws
- Government service procedures
- Tax regulations and business requirements
- Cultural traditions and tourism information
- Festival calendars and cultural etiquette

### Updating Knowledge Base
Add new information by editing JSON files in the `data/` directory:
```json
// data/civil_service.json
{
  "new_procedure": {
    "requirements": ["list", "of", "requirements"],
    "process": ["step", "by", "step", "process"],
    "documents": ["required", "documents"]
  }
}
```

## 🎨 Customization

### UI Themes
Modify CSS variables in `static/css/styles.css`:
```css
:root {
  --primary: #FF6B2C;        /* Orange from Bhutanese flag */
  --secondary: #4A90E2;      /* Sky blue */
  --accent: #FFD700;         /* Golden */
}
```

### Adding New Agents
1. Create new agent file in `agents/` directory
2. Implement the agent class with `process_query` method
3. Register the agent in `app.py`
4. Add agent information to the frontend

### Language Support
Extend language support by:
1. Adding translations to `utils/language_utils.py`
2. Updating HTML templates with data attributes
3. Adding language-specific suggestions

## 🔒 Security & Privacy

### Data Protection
- No user data is stored permanently without consent
- Chat history is stored locally in browser storage
- All API communications use HTTPS in production
- Sensitive government data is properly sanitized

### Authentication (Future)
- Government employee authentication
- Role-based access control
- Audit logging for official queries

## 📈 Performance

### Optimization
- Model responses cached for common queries
- Static assets served with appropriate caching headers
- Lazy loading for non-critical resources
- Service worker enables offline functionality

### Monitoring
- Health check endpoint at `/api/health`
- Error logging and monitoring
- Performance metrics collection

## 🤝 Contributing

### Development Guidelines
1. Follow Python PEP 8 style guidelines
2. Use meaningful commit messages
3. Test all changes thoroughly
4. Respect cultural sensitivity in all content
5. Maintain bilingual support

### Adding Features
1. Create feature branch from main
2. Implement changes with tests
3. Update documentation
4. Submit pull request with description

## 📞 Support

### Technical Support
- Email: support@sovereign.ai.bt
- Documentation: [Project Wiki]
- Issues: [GitHub Issues]

### Government Integration
For official government integration:
- Contact: Ministry of Information and Communications
- Email: mic@gov.bt
- Phone: +975-2-321953

## 📄 License

This project is developed for the Royal Government of Bhutan. All rights reserved.

For educational and research purposes, please contact the development team.

## 🙏 Acknowledgments

- Royal Government of Bhutan
- Ministry of Information and Communications  
- Bhutanese cultural advisors
- Open source AI community
- Ollama team for model serving capabilities

---

**Built with ❤️ for Gross National Happiness**

*འབྲུག་གི་སྤྱི་སྐུལ་དགའ་སྐྱིད་ཀྱི་དོན་དུ་བརྩམས་པ།*