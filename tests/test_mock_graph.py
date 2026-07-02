import pytest
from unittest.mock import patch, MagicMock
from src.state import VideoIntent
from src.graph import app

@patch("langchain_groq.ChatGroq")
def test_happy_path_mocked(mock_chat_groq):
    # 1. Setup a global mock for any time ChatGroq is called
    mock_llm_instance = MagicMock()
    mock_chat_groq.return_value = mock_llm_instance
    
    # Mock the structured output chain
    mock_chain = MagicMock()
    mock_llm_instance.with_structured_output.return_value = mock_chain
    
    # Define a script that passes ALL of your Phase 4 compiler checks
    valid_script = """
    import { Composition, Video } from 'remotion';
    const MyComposition = () => { return null; };
    export default MyComposition;
    """
    
    # Mock the final return values to simulate the LLMs passing valid data
    mock_chain.invoke.side_effect = [
        VideoIntent(pacing="fast", visual_style="energetic", caption_tone="fun", transition_preference="zoom"), 
        MagicMock(scenes=[]), 
        MagicMock(remotion_script=valid_script) 
    ]

    # 2. Initialize State
    initial_state = {"user_prompt": "Make a fun video", "retry_count": 0}

    # 3. Execute Graph
    final_state = app.invoke(initial_state)

    # 4. Assertions
    assert final_state["intent"].pacing == "fast"
    assert "export default" in final_state["remotion_script"]
    assert final_state["retry_count"] == 0