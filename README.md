# 🌟 AI Jyotish Guru - AstroHack Submission

AI-powered Vedic Astrology chatbot that combines ancient Jyotish wisdom with modern Generative AI to provide personalized, empathetic life guidance for Indian users.

## 🎯 Project Overview

This application fuses Vedic Astrology (Jyotish) with OpenAI's GPT models to create an intelligent, culturally-sensitive astrology consultant. It calculates accurate birth charts using Swiss Ephemeris and provides personalized guidance on:

- 💼 Career & Professional Growth
- 💑 Marriage & Relationships
- 💰 Finance & Wealth
- 🧘 Spiritual Development
- 📚 Education & Learning
- ⚕️ Health & Wellbeing

## ✨ Key Features

- **Accurate Vedic Calculations**: Uses Swiss Ephemeris for precise planetary positions
- **AI-Powered Insights**: OpenAI GPT-4 provides contextual, empathetic responses
- **Cultural Sensitivity**: Designed specifically for Indian cultural context
- **Grounded Responses**: AI interpretations are always based on actual chart data
- **Multiple Focus Areas**: Specialized guidance for different life aspects
- **Real-time Chat Interface**: Natural conversation flow
- **Responsive Design**: Works on desktop and mobile

## 🏗️ Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Astrology Engine**: PySwissEph (Swiss Ephemeris)
- **AI/LLM**: OpenAI GPT-4-Turbo API
- **Validation**: Pydantic
- **Geolocation**: Geopy, TimezoneFinder

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Icons**: React Icons
- **Notifications**: React Toastify
- **Styling**: Custom CSS with CSS Variables

### External APIs
- OpenAI GPT-4omini
- Swiss Ephemeris (astronomical calculations)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API Key

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your OpenAI API key to .env
OPENAI_API_KEY=your_key_here

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## 🤖 AI Model Information

This application uses **GPT-4o Mini** from OpenAI, which offers:

- ✅ **Cost-effective**: ~80% cheaper than GPT-4 Turbo
- ✅ **Fast responses**: Lower latency for better user experience
- ✅ **High quality**: Excellent performance for conversational tasks
- ✅ **128K context window**: Handles long conversations effectively
- ✅ **Multilingual**: Better support for Indian languages (future enhancement)

### Model Comparison

| Feature | GPT-4o Mini | GPT-4 Turbo |
|---------|-------------|-------------|
| Cost per 1M tokens (input) | $0.15 | $10.00 |
| Cost per 1M tokens (output) | $0.60 | $30.00 |
| Speed | Faster | Fast |
| Context Window | 128K | 128K |
| Quality | Excellent | Excellent+ |
| Best for | Conversational AI, Chat | Complex reasoning |

For this astrological guidance application, GPT-4o Mini provides the perfect balance of quality, speed, and cost-efficiency.

### API Cost Estimation

Typical chat interaction:
- Birth chart summary: ~800 tokens
- User message: ~50 tokens  
- AI response: ~400 tokens
- **Total per interaction**: ~1,250 tokens

**Cost per interaction**: ~$0.0009 (less than 0.1 cent)

For a hackathon with 100 test conversations: **~$0.09**