from langchain_groq import ChatGroq
from src.state import GraphState, Storyboard

def storyboard_writer_node(state: GraphState):
    print("--- RUNNING STORYBOARD WRITER AGENT ---")
    
    # Extract necessary context from the state
    intent = state.get("intent")
    selected_images = state.get("selected_images", [])
    
  # Initialize our fast Groq model
    llm = ChatGroq(
        model="llama-3.1-8b-instant", # <-- UPDATED MODEL
        temperature=0.7
    )

    # Bind our Pydantic model to force structured JSON output
    structured_llm = llm.with_structured_output(Storyboard)
    
    prompt = f"""
    You are a professional video storyboard director. 
    Based on the following user intent and selected images, create a cohesive storyboard.
    
    User Intent Pacing: {intent.pacing if intent else 'Medium'}
    User Intent Style: {intent.visual_style if intent else 'Standard'}
    User Intent Tone: {intent.caption_tone if intent else 'Neutral'}
    
    Selected Images: {selected_images}
    
    Assign appropriate captions, durations, and transitions for each scene to match the requested pacing and tone.
    """
    
    # Execute the structured LLM call
    storyboard_output = structured_llm.invoke(prompt)
    
    # Return the updated state
    return {"storyboard": storyboard_output}