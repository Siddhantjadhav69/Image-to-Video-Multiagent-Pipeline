from langgraph.graph import StateGraph, END
from src.state import GraphState
from src.parser import prompt_parser_node
from src.agents.image_analyser import image_analyser_node
from src.agents.storyboard_writer import storyboard_writer_node
from src.agents.script_generator import script_generator_node
from src.agents.compiler_fixer import compiler_fixer_node
from src.agents.renderer import renderer_node

# 1. Initialize the State Graph with our explicit GraphState schema
workflow = StateGraph(GraphState)

# 2. Add all 6 nodes to the graph
workflow.add_node("prompt_parser", prompt_parser_node)
workflow.add_node("image_analyser", image_analyser_node)
workflow.add_node("storyboard_writer", storyboard_writer_node)
workflow.add_node("script_generator", script_generator_node)
workflow.add_node("compiler_fixer", compiler_fixer_node)
workflow.add_node("renderer", renderer_node)

# 3. Define the routing conditional logic
def route_after_compiler(state: GraphState):
    """Checks for errors or if we need to loop back or exit."""
    if state.get("error_context") and state.get("retry_count", 0) < 3:
        print("--> Error detected! Routing back to Script Generator.")
        return "script_generator"
    elif state.get("error_context"):
        print("--> Max retries reached. Exiting with error.")
        return END
    else:
        print("--> Code validation passed! Routing to Renderer.")
        return "renderer"

# 4. Set entry point and map edges
workflow.set_entry_point("prompt_parser")
workflow.add_edge("prompt_parser", "image_analyser")
workflow.add_edge("image_analyser", "storyboard_writer")
workflow.add_edge("storyboard_writer", "script_generator")
workflow.add_edge("script_generator", "compiler_fixer")

# Add conditional routing out of the Compiler node
workflow.add_conditional_edges(
    "compiler_fixer",
    route_after_compiler,
    {
        "script_generator": "script_generator",
        "renderer": "renderer",
        END: END
    }
)

workflow.add_edge("renderer", END)

# 5. Compile the executable graph pipeline
app = workflow.compile()

# Test runner block
if __name__ == "__main__":
    initial_state = {
        "user_prompt": "Create a fast-paced cinematic video showcasing real estate properties with upbeat text options.",
        "selected_images": [],
        "storyboard": {},
        "remotion_script": "",
        "error_context": "",
        "retry_count": 0
    }
    
    print("Starting pipeline execution...")
    app.invoke(initial_state)