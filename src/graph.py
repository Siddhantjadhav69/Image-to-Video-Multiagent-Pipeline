from langgraph.graph import StateGraph, END
from src.state import GraphState
from src.parser import parser_node
from src.agents.image_analyser import image_analyser_node
from src.agents.storyboard_writer import storyboard_writer_node
from src.agents.script_generator import script_generator_node
from src.agents.compiler_fixer import compiler_fixer_node
from src.agents.renderer import renderer_node

# 1. Define the Conditional Routing Logic
def route_compiler_output(state: GraphState):
    error_context = state.get("error_context", "")
    retry_count = state.get("retry_count", 0)
    
    if not error_context:
        print("--- ROUTING: Validation Passed -> Proceeding to Renderer ---")
        return "renderer"
        
    if retry_count >= 3:
        print("--- ROUTING: Hard Cap Reached (3 Retries) -> Exiting Gracefully ---")
        return END
        
    print(f"--- ROUTING: Validation Failed (Attempt {retry_count}/3) -> Looping back to Script Generator ---")
    return "script_generator"

# 2. Build the Graph
workflow = StateGraph(GraphState)

# Add all nodes
workflow.add_node("parser", parser_node)
workflow.add_node("image_analyser", image_analyser_node)
workflow.add_node("storyboard_writer", storyboard_writer_node)
workflow.add_node("script_generator", script_generator_node)
workflow.add_node("compiler_fixer", compiler_fixer_node)
workflow.add_node("renderer", renderer_node)

# Set the entry point
workflow.set_entry_point("parser")

# Add the standard linear edges
workflow.add_edge("parser", "image_analyser")
workflow.add_edge("image_analyser", "storyboard_writer")
workflow.add_edge("storyboard_writer", "script_generator")
workflow.add_edge("script_generator", "compiler_fixer")

# 3. Add the Smart Conditional Edge
workflow.add_conditional_edges(
    "compiler_fixer",
    route_compiler_output,
    {
        "renderer": "renderer",
        "script_generator": "script_generator",
        END: END
    }
)

# Add the final exit edge
workflow.add_edge("renderer", END)

# Compile the final application
app = workflow.compile()

# Execution Block
if __name__ == "__main__":
    print("Starting Phase 4 self-healing pipeline execution...")
    initial_state = {
        "user_prompt": "Create a fast-paced, highly energetic promotional video using these 10 photos.",
        "retry_count": 0
    }
    
    final_state = app.invoke(initial_state)
    print("\n--- FINAL STATE OUTPUT ---")
    print(final_state)