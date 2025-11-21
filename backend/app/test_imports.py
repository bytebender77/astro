# app/test_imports.py
print("Testing imports...")

try:
    from app.astrology.chart_calculator import VedicChartCalculator
    print("✅ VedicChartCalculator imported successfully")
except Exception as e:
    print(f"❌ Error importing VedicChartCalculator: {e}")

try:
    from app.ai.chatbot import AstroAIChatbot
    print("✅ AstroAIChatbot imported successfully")
except Exception as e:
    print(f"❌ Error importing AstroAIChatbot: {e}")

try:
    from app.ai.prompts import SYSTEM_PROMPT, get_context_prompt
    print("✅ Prompts imported successfully")
except Exception as e:
    print(f"❌ Error importing prompts: {e}")

print("\n✅ All imports successful!")