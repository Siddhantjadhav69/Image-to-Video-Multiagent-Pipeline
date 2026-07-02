from langgraph.graph import StateGraph, END
from src.state import GraphState

# Import your functional nodes
from src.parser import prompt_parser_node
from src.agents.image_analyser import image_analyser_node
from src.agents.storyboard_writer import storyboard_writer_node
from src.agents.script_generator import script_generator_node

# Import the placeholder nodes for Phase 4
from src.agents.compiler_fixer import compiler_fixer_node
from src.agents.renderer import renderer_node

def build_graph():
    # Initialize the state graph
    workflow = StateGraph(GraphState)
    
    # 1. Add the Nodes
    workflow.add_node("parser", prompt_parser_node)
    workflow.add_node("image_analyser", image_analyser_node)
    workflow.add_node("storyboard_writer", storyboard_writer_node)
    workflow.add_node("script_generator", script_generator_node)
    workflow.add_node("compiler_fixer", compiler_fixer_node)
    workflow.add_node("renderer", renderer_node)
    
    # 2. Define the Linear Edges
    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "image_analyser")
    workflow.add_edge("image_analyser", "storyboard_writer")
    workflow.add_edge("storyboard_writer", "script_generator")
    workflow.add_edge("script_generator", "compiler_fixer")
    
    # For now, we will statically route to the renderer. 
    # In Phase 4, we will make this a conditional edge for the retry loop.
    workflow.add_edge("compiler_fixer", "renderer")
    workflow.add_edge("renderer", END)
    
    # 3. Compile the Graph
    app = workflow.compile()
    return app

if __name__ == "__main__":
    print("Starting Phase 3 pipeline execution...")
    
    # Initialize a mock state to test the pipeline
    initial_state = {
        "user_prompt": "Create a fast-paced, highly energetic promotional video using these 10 photos.",
        "retry_count": 0
    }
    
    app = build_graph()
    
    # Execute the graph
    final_state = app.invoke(initial_state)
    
    print("\n--- FINAL STATE OUTPUT ---")
    print(final_state)