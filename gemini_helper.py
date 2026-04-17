import os
from dotenv import load_dotenv
from google import genai  # Modern import
from google.genai import types

load_dotenv()

# Initialize the client with your API key
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini(question, data_preview=None, summary_stats=None):
    """
    Ask Gemini AI a question with financial data context using system instructions.
    """
    system_instruction = "You are a personal finance assistant AI with expertise in financial analysis, budgeting, and investment advice."

    # Prepare context strings
    context = ""
    if data_preview and summary_stats:
        context = f"\nCONTEXT - User's Financial Data:\n{summary_stats}\n\nRecent Transactions:\n{data_preview}"

    # Build prompt with instructions
    full_prompt = f"{context}\n\nUSER QUESTION: {question}\n\nINSTRUCTIONS:\n- Provide specific, actionable insights based on data.\n- Use numbers and percentages.\n- If data is missing for an answer, state it clearly."

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction, # Cleaner persona management
                temperature=0.7 # Balancing creativity and factual accuracy
            ),
            contents=full_prompt
        )
        return response.text.strip()

    except Exception as e:
        # Consider logging the error here
        return f"Error: {str(e)}"
