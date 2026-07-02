import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.state import GraphState, VideoIntent

load_dotenv()

def parser_node(state: GraphState) -> dict:
    """
    Parses the raw user prompt into a structured format containing
    pacing, visual style, caption tone, and transition preferences using Groq.
    """
    print("\n--- RUNNING PROMPT PARSER NODE (GROQ) ---")
    user_prompt = state.get("user_prompt", "")
    
    if not user_prompt:
        return {"error_context": "No user prompt provided.", "intent": None}
    
    # Initialize the Groq LLM with structured output tracking
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    structured_llm = llm.with_structured_output(VideoIntent)
    
    try:
        # Request structured parsing from the model
        parsed_intent = structured_llm.invoke(
            f"Analyze this video creation prompt and extract the style attributes: {user_prompt}"
        )
        return {"intent": parsed_intent}
    except Exception as e:
        return {"error_context": f"Failed to parse prompt via Groq: {str(e)}"}