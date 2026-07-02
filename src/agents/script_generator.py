from langchain_groq import ChatGroq
from src.state import GraphState, RemotionScript

def script_generator_node(state: GraphState):
    print("--- RUNNING SCRIPT GENERATOR AGENT ---")
    
    # Extract the necessary context
    intent = state.get("intent")
    storyboard = state.get("storyboard")
    
    # In a full implementation, you would query your local vector store here:
    # retrieved_api_docs = vector_store.similarity_search("Remotion useVideoConfig useCurrentFrame")
    retrieved_api_docs = "Assume context for standard Remotion hooks is injected here."
    
    # Initialize our heavy-duty Groq model for coding
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", # <-- UPDATED MODEL
        temperature=0.2 
    )
    
    # Bind our Pydantic model to force structured output
    structured_llm = llm.with_structured_output(RemotionScript)
    
    prompt = f"""
    You are an expert React and Remotion developer. 
    Based on the following storyboard and video intent, write a fully runnable Remotion composition script.
    
    Visual Style: {intent.visual_style if intent else 'Standard'}
    Storyboard: {storyboard}
    
    Relevant Remotion API Context:
    {retrieved_api_docs}
    
    Ensure the code is syntactically correct, uses appropriate Remotion hooks (like useVideoConfig and useCurrentFrame), and returns ONLY the structured code block.
    """
    
    # Execute the structured LLM call
    script_output = structured_llm.invoke(prompt)
    
    # Return the updated state
    return {"remotion_script": script_output.code}