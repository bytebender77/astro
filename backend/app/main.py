from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv

from app.astrology.chart_calculator import VedicChartCalculator
from app.ai.chatbot import AstroAIChatbot
from app.models import BirthData, ChatMessage, ChatRequest

load_dotenv()

app = FastAPI(
    title="AstroHack AI Jyotish API",
    description="AI-powered Vedic Astrology Guidance System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chart_calculator = VedicChartCalculator()
chatbot = AstroAIChatbot(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Updated default
)

# In-memory storage (use Redis/DB in production)
user_sessions = {}


@app.get("/")
async def root():
    return {
        "message": "AstroHack AI Jyotish API",
        "version": "1.0.0",
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "endpoints": ["/birth-chart", "/chat", "/health"]
    }


@app.post("/birth-chart")
async def calculate_birth_chart(birth_data: BirthData):
    """Calculate Vedic birth chart"""
    try:
        chart_data = chart_calculator.calculate_chart(
            date=birth_data.date,
            time=birth_data.time,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # Store in session
        session_id = birth_data.session_id or f"session_{len(user_sessions)}"
        user_sessions[session_id] = {
            "birth_data": birth_data.dict(),
            "chart_data": chart_data,
            "conversation_history": []
        }
        
        return {
            "session_id": session_id,
            "chart_data": chart_data,
            "message": "Birth chart calculated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat interaction"""
    try:
        session_id = request.session_id
        
        if session_id not in user_sessions:
            raise HTTPException(status_code=404, detail="Session not found. Please create a birth chart first.")
        
        session = user_sessions[session_id]
        chart_data = session["chart_data"]
        conversation_history = session["conversation_history"]
        
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": request.message
        })
        
        # Get AI response
        response = await chatbot.get_response(
            user_message=request.message,
            chart_data=chart_data,
            conversation_history=conversation_history,
            context=request.context
        )
        
        # Add AI response to history
        conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Keep only last 20 messages
        session["conversation_history"] = conversation_history[-20:]
        
        return {
            "response": response,
            "session_id": session_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini")}