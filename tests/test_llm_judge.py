import pytest
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class CoherenceScore(BaseModel):
    score: int = Field(description="Score from 1 to 10 evaluating narrative coherence.")
    reasoning: str = Field(description="Brief explanation of the score.")

def test_storyboard_coherence_with_llm():
    # 1. Initialize the Judge Model
    judge_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    ).with_structured_output(CoherenceScore)
    
   # 2. Sample output from your pipeline
    sample_storyboard = """
    Scene 1 (The Beginning): 'The starting line. Nerves are high as the runners take their marks.' (Image: start_line.jpg, Transition: fade in)
    Scene 2 (The Middle): 'Mid-race. Pushing through the pain, our lead runner breaks away from the pack.' (Image: running_pack.jpg, Transition: wipe)
    Scene 3 (The End): 'Victory! Crossing the finish line in first place.' (Image: finish_line.jpg, Transition: zoom out)
    """

    # 3. The Evaluation Prompt
    prompt = f"""
    You are an expert video director. Evaluate the following storyboard for a short promotional video.
    Does it have a logical beginning (setting the scene), middle (the main action), and end (the resolution)?
    
    Score a 10 if there is a clear start, action, and resolution. Be generous if the scenes logically follow one another.
    
    Storyboard:
    {sample_storyboard}
    """

    # 4. Get Judgment
    evaluation = judge_llm.invoke(prompt)

    # 5. Assert it passes our quality threshold (e.g., score >= 7)
    print(f"LLM Judge Reasoning: {evaluation.reasoning}")
    assert evaluation.score >= 7