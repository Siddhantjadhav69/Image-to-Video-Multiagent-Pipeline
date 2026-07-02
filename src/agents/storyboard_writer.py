import os
import json
from groq import Groq
# Adjust the import path based on your project structure
from src.rag.vector_store import DocumentStore

# Ensure GROQ_API_KEY is in your environment
client = Groq()
db = DocumentStore()

def generate_storyboard(video_intent: str, selected_images: list[int], style_preference: str) -> dict:
    """Generates a structured storyboard using RAG context and Groq."""
    
    # 1. Retrieve Style Context from RAG
    print(f"Retrieving style guidelines for: '{style_preference}'...")
    style_results = db.query_documents("video_styles", style_preference, n_results=1)
    
    # Safely extract the document context
    if style_results and style_results.get('documents') and style_results['documents'][0]:
        style_context = style_results['documents'][0][0]
    else:
        style_context = "Use standard pacing and simple cut transitions."

    # 2. Construct the Prompt
    system_prompt = (
        "You are an expert video director. Your job is to create a JSON storyboard for a video "
        "based on the user's intent, the provided style guide, and the selected images.\n\n"
        f"CRITICAL STYLE GUIDE TO FOLLOW: {style_context}\n\n"
        "Return ONLY a valid JSON object with a 'scenes' array. Each scene object must contain:\n"
        "- 'scene_number' (integer)\n"
        "- 'image_index' (integer, must be chosen from the provided Available Selected Images)\n"
        "- 'duration_seconds' (integer or float, pacing based on the style guide)\n"
        "- 'transition_out' (string, e.g., 'fade', 'cut', 'wipe', based on the style guide)"
    )
    
    user_prompt = (
        f"User Intent: {video_intent}\n"
        f"Available Selected Images (Indices): {selected_images}\n"
        "Generate the storyboard."
    )

    # 3. Call the LLM with JSON mode forced
    response = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2, # Low temperature for logical consistency
        response_format={"type": "json_object"}
    )
    
    try:
        storyboard = json.loads(response.choices[0].message.content)
        return storyboard
    except json.JSONDecodeError:
        print("Failed to parse JSON storyboard. Raw output:", response.choices[0].message.content)
        return {"scenes": []}

# Quick test
if __name__ == "__main__":
    # Simulating data passed from the Image Analyser
    mock_intent = "A fast-paced energetic highlight reel"
    mock_images = [1, 3, 4] # The indices chosen by the vision model
    mock_style = "energetic and upbeat"
    
    result = generate_storyboard(mock_intent, mock_images, mock_style)
    print(json.dumps(result, indent=2))