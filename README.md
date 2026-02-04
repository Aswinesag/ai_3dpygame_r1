# 🎮 AI 3D PyGame Code Generator

A powerful Streamlit application that generates PyGame code using AI reasoning and visualization capabilities. This app combines Groq's free reasoning model with OpenAI's code generation to create interactive PyGame visualizations.

## ✨ Features

### 🧠 AI-Powered Code Generation
- **Groq Reasoning Engine**: Uses `llama-3.1-8b-instant` model for intelligent reasoning
- **OpenAI Code Extraction**: Leverages GPT-4o for clean Python code extraction
- **Free Alternative**: Replaces limited DeepSeek R1 with unlimited Groq usage

### 🎯 PyGame Specialization
- **Expert System**: Specialized prompts for PyGame and Python programming
- **Code Quality**: Generates well-structured, executable PyGame scripts
- **Visual Explanations**: Includes reasoning and code explanations

### 🌐 Browser Integration
- **One-Click Visualization**: Opens generated code in browser with formatted display
- **Trinket Integration**: Direct access to Trinket PyGame editor
- **Manual Fallback**: Clear instructions for copy-paste execution

### 🛠️ User Experience
- **Clean Interface**: Modern Streamlit UI with intuitive controls
- **Real-time Feedback**: Progress indicators and error handling
- **Code Display**: Syntax-highlighted code with expandable sections

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API keys for Groq and OpenAI

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_3dpygame_r1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   streamlit run ai_3dpygame_r1.py
   ```

### API Keys Setup

You'll need API keys from:

1. **Groq** (Free):
   - Sign up at [console.groq.com](https://console.groq.com/)
   - Get your API key from the dashboard
   - Free tier: 30 requests/minute, 14,400 requests/day

2. **OpenAI**:
   - Sign up at [platform.openai.com](https://platform.openai.com/)
   - Create an API key from the API section

Add them to your `.env` file:
```env
groq=your_groq_api_key_here
openai=your_openai_api_key_here
```

## 📖 Usage Guide

### 1. Generate PyGame Code
1. Enter your PyGame query in the text area
2. Example: *"Create a particle system simulation where 100 particles emit from the mouse position and respond to keyboard-controlled wind forces"*
3. Click "Generate Code"

### 2. View Reasoning
- Expand "Groq's Reasoning" to see the AI's thought process
- Understand how the code was conceptualized

### 3. Generate Visualization
1. Click "Generate Visualization" after code generation
2. Two browser tabs will open:
   - Formatted HTML page with your code and instructions
   - Trinket PyGame editor
3. Copy the code and paste it into Trinket
4. Click Run (▶) to execute

## 🏗️ Architecture

### AI Pipeline
```
User Query → Groq Reasoning → OpenAI Extraction → PyGame Code → Browser Visualization
```

### Technology Stack
- **Frontend**: Streamlit
- **AI Models**: Groq (llama-3.1-8b-instant) + OpenAI (gpt-4o)
- **Browser**: Python webbrowser module
- **Environment**: Python-dotenv for configuration

### Key Components
- **Reasoning Engine**: Groq for intelligent problem-solving
- **Code Extractor**: OpenAI for clean Python code generation
- **Visualization**: HTML generation and browser automation
- **Error Handling**: Comprehensive fallback mechanisms

## 🎯 Example Queries

Try these sample queries to test the system:

### Basic Animations
```
Create a bouncing ball animation with gravity physics and color changes on collision
```

### Interactive Systems
```
Build a particle system where particles follow the mouse and respond to keyboard controls
```

### Games
```
Design a simple Pong game with two paddles, ball physics, and score tracking
```

### Visual Effects
```
Generate a fireworks display with colorful particle explosions and gravity effects
```

## 🔧 Configuration

### Environment Variables
```env
# Required
groq=your_groq_api_key
openai=your_openai_api_key

# Optional (for future browser automation)
BROWSER_USE_API_KEY=your_browser_use_key
```

### Model Parameters
- **Groq Model**: `llama-3.1-8b-instant`
- **OpenAI Model**: `gpt-4o`
- **Max Tokens**: 4000 for reasoning
- **Temperature**: 0.1 for consistent output

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify keys are correctly set in `.env`
   - Check API key permissions and quotas

2. **Browser Issues**
   - Ensure default browser is set
   - Check pop-up blocker settings

3. **Code Execution**
   - Verify PyGame syntax in Trinket
   - Check for missing imports or dependencies

### Error Messages
- **"Please provide both API keys"**: Add missing API keys to sidebar
- **"BROWSER_USE_API_KEY not found"**: Set environment variable (optional)
- **"Error running code on Trinket"**: Use manual fallback option

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Test thoroughly
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add comprehensive comments
- Include error handling
- Test with various PyGame queries

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** - For providing free, fast reasoning models
- **OpenAI** - For powerful code generation capabilities
- **Trinket** - For accessible PyGame execution environment
- **Streamlit** - For the excellent web framework

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Include error messages and system details

---

**🚀 Start creating amazing PyGame visualizations with AI today!**
