import os
import base64
import json
from groq import Groq

# Ensure your GROQ_API_KEY is in your environment variables
client = Groq()

def encode_image(image_path: str) -> str:
    """Helper to convert local image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_images(image_paths: list[str], video_intent: str) -> dict:
    """Analyzes images and selects the best subset based on intent."""
    
    # Construct the message payload with multiple images
    content = [
        {
            "type": "text",
            "text": f"You are a video editor. The user intent is: '{video_intent}'. "
                    f"Analyze these images. Return ONLY a JSON object with two keys: "
                    f"'selected_images' (a list of 1-based indices of the images you chose) and "
                    f"'reasoning' (a brief string explaining why). Do not include markdown formatting or extra text."
        }
    ]

    for img_path in image_paths:
        base64_img = encode_image(img_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_img}"
            }
        })

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[{"role": "user", "content": content}],
        temperature=0.1, # Low temperature for more deterministic JSON output
    )

    try:
        # Parse the strict JSON output
        result = json.loads(response.choices[0].message.content)
        return result
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:", response.choices[0].message.content)
        return {"selected_images": [], "reasoning": "Failed to parse"}

# Quick test
if __name__ == "__main__":
    # Replace with a couple of actual dummy image paths in your project
    dummy_images = ["./test_img1.jpg", "./test_img2.jpg"] 
    intent = "A cinematic highlight reel of a nature trek"
    
    # print(analyze_images(dummy_images, intent))