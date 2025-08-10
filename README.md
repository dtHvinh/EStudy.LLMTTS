# AI Voice Chat Assistant

A real-time AI-powered voice chat application built with FastAPI, featuring streaming text-to-speech synthesis and WebSocket communication. This project provides both Piper TTS and Coqui TTS integration for high-quality voice synthesis.

## 🎯 Features

- **Real-time Voice Chat**: WebSocket-based communication with AI assistant
- **Streaming TTS**: Real-time audio synthesis with Piper TTS
- **TTS Engines**: Piper TTS
- **AI Integration**: OpenAI GPT models
- **Personality System**: Configurable AI personalities through markdown prompts
- **Web Interface**: Modern HTML/JavaScript chat interface

## 📋 Prerequisites

- **Python 3.10+** (Required for this project)
- **Git** (for cloning the repository)
- **OpenAI API Key** (for GPT models)

### System Requirements

- **Windows**: Tested on Windows (PowerShell)
- **RAM**: 4GB+ recommended
- **Storage**: 2GB+ for models and dependencies

## 🚀 Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/dtHvinh/EStudy.LLMTTS.git
cd ai
```

### 2. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv env_realtimetts

# Activate virtual environment
.\env_realtimetts\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install core dependencies
pip install fastapi uvicorn
pip install python-dotenv
pip install websockets
pip install openai

# Install TTS engines
pip install piper-tts

# Install additional dependencies
pip install python-multipart
pip install jinja2
```

### 4. Download Voice Models

#### For Piper TTS:

1. Visit [Piper TTS Models](https://github.com/rhasspy/piper/releases)
2. Download a voice model (e.g., `en_US-hfc_female-medium.tar.gz`)
3. Extract to `D:\dev\AI\Voices\en_US-hfc_female-medium\`
4. Update the `VOICE_PATH` in the code if different

### 5. Environment Configuration

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

### 6. Verify Installation

```powershell
# Test Python imports
python -c "import fastapi, piper, openai; print('All imports successful!')"

# Check if Piper voice model exists
python -c "from piper import PiperVoice; print('Piper TTS ready!')"
```

## 🏃‍♀️ Running the Application

### Development Server

```powershell
# Activate virtual environment (if not already active)
.\env_realtimetts\Scripts\Activate.ps1

# Run FastAPI development server
python -m fastapi dev app.py

# Alternative using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Using VS Code Tasks

If using VS Code, you can run the predefined task:

1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Run FastAPI Dev Server"

## 🌐 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Open the chat interface: `http://localhost:8000/chat.html`
3. Start chatting with the AI assistant!

### API Endpoints

#### REST API

- `POST /api/voice_chat` - Voice chat with streaming response

#### WebSocket Endpoints

- `ws://localhost:8000/ws/chat/{conversation_id}` - Real-time voice chat (Piper TTS)

### Testing

```powershell
# Test TTS functionality
python tests/tts_comparison.py

# Test OpenAI integration
python tests/openai_test.py

# Test HTTP endpoints
python tests/http-test.py
```

## 📁 Project Structure

```
ai/
├── app.py                    # Main FastAPI application
├── chat.html                 # Web chat interface
├── piper_test.html          # TTS testing interface
├── .env                     # Environment variables (create this)
├── constants/
│   └── symbol.py            # Application constants
├── helper/
│   └── prompt_loader.py     # Prompt management utilities
├── managers/
│   └── websocket_manager.py # WebSocket connection management
├── prompts/                 # AI personality configurations
│   ├── Lexa.md             # Default AI personality
│   ├── RealPerson.md       # Natural conversation style
│   ├── Tutor.md            # English learning assistant
│   └── Translator.md       # Dictionary assistant
├── routers/
│   ├── ai_conversation/    # Chat API endpoints
│   ├── ai_dict/           # Dictionary API
│   └── websocket/         # WebSocket endpoints
└── tests/                 # Test scripts
```

## ⚙️ Configuration

### Voice Models

Update voice model paths in the respective files:

- `routers/ai_conversation/endpoint.py`
- `routers/websocket/endpoint.py`

```python
VOICE_PATH = r"D:\path\to\your\voice\model.onnx"
```

### AI Personalities

Customize AI behavior by editing files in the `prompts/` directory:

- `Lexa.md` - Technical assistant personality
- `RealPerson.md` - Natural conversation style
- `Tutor.md` - English learning assistant
- `Translator.md` - Dictionary responses

### OpenAI Models

Update model names in the endpoints as needed:

```python
model="gpt-4o-mini"  # or "gpt-3.5-turbo", "gpt-4", etc.
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Error: piper module not found**

   ```powershell
   pip install piper-tts
   ```

2. **Voice model not found**

   - Check the `VOICE_PATH` in your code
   - Ensure the `.onnx` file exists at the specified location

3. **OpenAI API Error**

   - Verify your API key in the `.env` file
   - Check your OpenAI account credits

4. **Port already in use**

   ```powershell
   # Use a different port
   uvicorn app:app --reload --port 8001
   ```

5. **WebSocket connection issues**
   - Check firewall settings
   - Ensure the server is running
   - Verify the WebSocket URL

## 📚 API Documentation

Once the server is running, visit:

- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Piper TTS](https://github.com/rhasspy/piper) - Fast neural text-to-speech
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenAI](https://openai.com/) - GPT models and API

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the project logs for error messages
3. Open an issue on the repository with detailed information

---

**Happy chatting with your AI assistant! 🤖💬**
