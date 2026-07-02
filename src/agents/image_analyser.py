from src.state import GraphState

def image_analyser_node(state: GraphState) -> dict:
    print("--- RUNNING IMAGE ANALYSER AGENT ---")
    # Mocking selecting 3 images
    return {"selected_images": ["image1.jpg", "image2.jpg", "image3.jpg"]}