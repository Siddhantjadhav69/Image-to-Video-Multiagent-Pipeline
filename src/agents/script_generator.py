import json
from groq import Groq

# Ensure GROQ_API_KEY is in your environment
client = Groq()

def generate_script(video_intent: str, storyboard: dict, tone: str) -> dict:
    """Generates scene-by-scene voiceover script matching the storyboard timeline."""
    
    system_prompt = (
        "You are an expert scriptwriter for short-form video content. "
        "Your job is to write compelling, perfectly timed voiceover lines (or on-screen text) "
        "for each scene in the provided storyboard. Keep the tone strictly aligned with the requested style.\n\n"
        "Return ONLY a valid JSON object with a 'script' array. Each object in the array must contain:\n"
        "- 'scene_number' (integer, matching the storyboard)\n"
        "- 'voiceover_text' (string, concise enough to be spoken within the scene's 'duration_seconds')\n"
        "- 'overlay_text' (string, a 2-4 word punchy summary for the screen)"
    )
    
    user_prompt = (
        f"Video Intent: {video_intent}\n"
        f"Requested Tone: {tone}\n"
        f"Storyboard JSON Blueprint:\n{json.dumps(storyboard, indent=2)}\n\n"
        "Generate the script."
    )

    print("Generating script based on storyboard timing...")
    
    response = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6, # Slightly higher for creative copy, but grounded by the prompt
        response_format={"type": "json_object"}
    )
    
    try:
        script_data = json.loads(response.choices[0].message.content)
        return script_data
    except json.JSONDecodeError:
        print("Failed to parse JSON script. Raw output:", response.choices[0].message.content)
        return {"script": []}

# Quick test
if __name__ == "__main__":
    # Simulating the output from your Storyboard Writer
    mock_intent = "A fast-paced energetic highlight reel"
    mock_tone = "energetic and upbeat"
    mock_storyboard = {
        "scenes": [
            {"scene_number": 1, "image_index": 1, "duration_seconds": 2.5, "transition_out": "wipe"},
            {"scene_number": 2, "image_index": 3, "duration_seconds": 3.0, "transition_out": "cut"}
        ]
    }
    
    result = generate_script(mock_intent, mock_storyboard, mock_tone)
    print(json.dumps(result, indent=2))