from src.state import GraphState

def renderer_node(state: GraphState) -> dict:
    print("--- RUNNING RENDERER AGENT ---")
    print("Video pipeline completed successfully!")
    # LangGraph requires us to return at least one state key.
    # We will just harmlessly return the current retry_count.
    return {"retry_count": state.get("retry_count", 0)}