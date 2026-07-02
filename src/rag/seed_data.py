from vector_store import DocumentStore

def seed_database():
    store = DocumentStore()

    # 1. Seed Style Guides
    styles = [
        "Cinematic: Use slow pans, letterboxing, and high-contrast color grading. Transitions should be slow crossfades.",
        "Upbeat: Fast cuts, vibrant saturation, and dynamic zoom-ins on beat drops. Use slide and wipe transitions."
    ]
    style_metadatas = [{"type": "style", "name": "cinematic"}, {"type": "style", "name": "upbeat"}]
    style_ids = ["style_001", "style_002"]
    
    store.add_documents("video_styles", styles, style_metadatas, style_ids)

    # 2. Seed Remotion Snippets
    remotion_docs = [
        "To render an image in Remotion, use the <Img src={...} /> component from 'remotion'. Ensure the src is a valid require() or static URL.",
        "For simple transitions, use the spring() function from 'remotion' to animate opacities or transforms smoothly based on the current frame."
    ]
    remotion_metadatas = [{"type": "api", "component": "Img"}, {"type": "api", "component": "spring"}]
    remotion_ids = ["api_001", "api_002"]

    store.add_documents("remotion_api", remotion_docs, remotion_metadatas, remotion_ids)

    # 3. Test Retrieval
    print("\n--- Testing Retrieval ---")
    results = store.query_documents("video_styles", "I need a fast-paced energetic video", n_results=1)
    print("Top match for 'energetic':", results['documents'][0])

if __name__ == "__main__":
    seed_database()