import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state import GraphState

def script_generator_node(state: GraphState):
    print("--- RUNNING SCRIPT GENERATOR AGENT (GROQ) ---")
    
    storyboard = state.get("storyboard")
    error_context = state.get("error_context", "")
    retry_count = state.get("retry_count", 0)
    
    # Initialize the heavy-duty model for code generation
    llm = ChatGroq(
        temperature=0.1, 
        model_name="llama-3.3-70b-versatile",
    )
    
    system_prompt = (
        "You are an expert React developer specializing in the Remotion library. "
        "Generate a fully runnable Remotion composition script based on the provided storyboard data. "
        "Return ONLY valid React code. Do NOT wrap the code in markdown backticks (```). Do NOT add explanations."
    )
    
    # Inject the RAG error documentation if this is a retry loop
    if error_context:
        print(f"--> [INFO] Applying RAG error context (Retry {retry_count}). Fixing code...")
        system_prompt += (
            f"\n\nCRITICAL FIX REQUIRED. Your previous attempt failed. "
            f"Here is the validation feedback and API documentation:\n{error_context}\n"
            f"Apply these fixes to the React code immediately."
        )
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Storyboard Data: {storyboard}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"storyboard": storyboard})
    
    # Clean any accidental markdown wrapping if the LLM disobeys the prompt
    clean_code = response.content.replace("```javascript", "").replace("```jsx", "").replace("```", "").strip()
    
    return {
        "remotion_script": clean_code
    }