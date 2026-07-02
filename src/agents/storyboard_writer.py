from src.state import GraphState

def storyboard_writer_node(state: GraphState) -> dict:
    print("--- RUNNING STORYBOARD WRITER AGENT ---")
    mock_storyboard = {"scenes": [{"image": "image1.jpg", "caption": "Welcome to our product showcase!"}]}
    return {"storyboard": mock_storyboard}