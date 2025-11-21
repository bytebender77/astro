from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json

from app.ai.prompts import SYSTEM_PROMPT, get_context_prompt


class AstroAIChatbot:
    """AI-powered Vedic Astrology Chatbot using OpenAI GPT-4o Mini"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        print(f"🤖 Initialized AstroAI Chatbot with model: {model}")
    
    async def get_response(
        self,
        user_message: str,
        chart_data: Dict,
        conversation_history: List[Dict],
        context: Optional[str] = None
    ) -> str:
        """
        Generate AI response based on user query and birth chart
        
        Args:
            user_message: User's question
            chart_data: Complete birth chart data
            conversation_history: Previous conversation
            context: Specific context (career, marriage, etc.)
        
        Returns:
            AI-generated response
        """
        # Prepare chart summary for AI
        chart_summary = self._prepare_chart_summary(chart_data)
        
        # Build messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Birth Chart Data:\n{chart_summary}"}
        ]
        
        # Add context-specific instructions
        if context:
            context_prompt = get_context_prompt(context)
            if context_prompt:
                messages.append({"role": "system", "content": context_prompt})
        
        # Add conversation history (last 8 messages for GPT-4o mini context)
        messages.extend(conversation_history[-8:])
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenAI API with GPT-4o Mini optimized parameters
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.75,  # Slightly higher for more natural responses
                max_tokens=1000,   # Increased for detailed responses
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.4  # Encourage diverse vocabulary
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg:
                return "I apologize, but the API quota has been exceeded. Please try again later or contact support."
            elif "invalid_api_key" in error_msg:
                return "API configuration error. Please contact support."
            else:
                return f"I apologize, but I encountered an error processing your request. Please try again. (Error: {error_msg})"
    
    def _prepare_chart_summary(self, chart_data: Dict) -> str:
        """Convert chart data to readable summary for AI"""
        
        planets_summary = []
        for planet, data in chart_data['planets'].items():
            strength_info = ""
            if planet in chart_data.get('strengths', {}):
                strength_info = f" - Strength: {chart_data['strengths'][planet]['status']}"
            
            planets_summary.append(
                f"• {planet}: {data['sign']} at {data['degree']}° in Nakshatra {data['nakshatra']}{strength_info}"
            )
        
        summary = f"""
═══════════════════════════════════════════════════════
VEDIC BIRTH CHART SUMMARY (Sidereal/Lahiri Ayanamsa)
═══════════════════════════════════════════════════════

🔹 ASCENDANT (LAGNA):
   {chart_data['ascendant']['sign']} at {chart_data['ascendant']['degree']}°

🔹 PLANETARY POSITIONS:
{chr(10).join(planets_summary)}

🔹 MOON'S NAKSHATRA (Birth Star):
   {chart_data['moon_nakshatra']['name']} - Pada {chart_data['moon_nakshatra']['pada']}
   Nakshatra Lord: {chart_data['moon_nakshatra']['lord']}

🔹 KEY INTERPRETATIONS:
   • Ascendant Sign: {chart_data['interpretation']['ascendant_sign']}
   • Moon Placement: {chart_data['interpretation']['moon_sign']}
   • Sun Placement: {chart_data['interpretation']['sun_sign']}

═══════════════════════════════════════════════════════
IMPORTANT: Base ALL interpretations strictly on this data.
Refer to specific planetary positions when answering.
═══════════════════════════════════════════════════════
"""
        return summary


__all__ = ['AstroAIChatbot']