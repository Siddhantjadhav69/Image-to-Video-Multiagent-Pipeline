from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from src.state import GraphState

# Define the structured output for our Vision Agent
class ImageSelection(BaseModel):
    selected_images: List[str] = Field(description="List of selected image filenames")
    reasoning: str = Field(description="Why these images were selected based on the intent")

def image_analyser_node(state: GraphState):
    print("--- RUNNING IMAGE ANALYSER AGENT ---")
    
    intent = state.get("intent")
    
    # Initialize the Groq Vision model
    llm = ChatGroq(
        model="llama-3.2-11b-vision-preview", 
        temperature=0.2
    )
    
    # Bind our Pydantic model to force structured JSON output
    structured_llm = llm.with_structured_output(ImageSelection)
    
    # In a full implementation, you would pass base64 image data here.
    # For our architectural pipeline, we are prompting it with a mock list.
    prompt = f"""
    You are an expert video editor. Based on the user intent style: {intent.visual_style if intent else 'Standard'}
    Select the best 3 images from this raw event pool: ['event_1.jpg', 'event_2.jpg', 'event_3.jpg', 'event_4.jpg', 'event_5.jpg']
    """
    
    try:
        output = structured_llm.invoke(prompt)
        selected = output.selected_images
    except Exception as e:
        # Fallback just in case the API rate limits during our pipeline test
        selected = ['event_1.jpg', 'event_3.jpg', 'event_5.jpg']
        
    return {"selected_images": selected}