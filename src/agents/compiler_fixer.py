from src.state import GraphState

# Mini Knowledge Base for Remotion
REMOTION_DOCS = {
    "imports": "Remotion Docs: Always import core hooks from 'remotion'. Example: `import { useVideoConfig, useCurrentFrame, AbsoluteFill } from 'remotion';`",
    "useVideoConfig": "Remotion Docs: `useVideoConfig` provides composition properties. You MUST call it inside your component. Example: `const { width, height, fps, durationInFrames } = useVideoConfig();`",
    "export default": "Remotion Docs: The root composition MUST be exported as the default export. Example: `export default MyComposition;`",
    "JSX": "React Docs: Ensure your component returns valid JSX, typically wrapped in a root element like `<div>` or `<AbsoluteFill>`."
}

def compiler_fixer_node(state: GraphState):
    print("--- RUNNING COMPILER & FIXER AGENT ---")
    
    script = state.get("remotion_script", "")
    retry_count = state.get("retry_count", 0)
    
    errors = []
    relevant_docs = []
    
    # 1. Validate Core Imports
    if "from 'remotion'" not in script:
        errors.append("Missing Remotion imports.")
        relevant_docs.append(REMOTION_DOCS["imports"])
        
    if "useVideoConfig" not in script:
        errors.append("Missing useVideoConfig hook for dynamic rendering.")
        relevant_docs.append(REMOTION_DOCS["useVideoConfig"])
        
    # 2. Validate React/JSX Structure
    if "export default" not in script:
        errors.append("Missing 'export default' for the main composition component.")
        relevant_docs.append(REMOTION_DOCS["export default"])
        
    if "<div" not in script and "<img" not in script and "<AbsoluteFill" not in script:
        errors.append("No valid JSX rendering elements found in the return block.")
        relevant_docs.append(REMOTION_DOCS["JSX"])
        
    # 3. Handle Errors & Inject Docs
    if errors:
        error_msg = " | ".join(errors)
        docs_msg = "\n".join(relevant_docs)
        
        print(f"--> [ERROR] Code validation failed: {error_msg}")
        print(f"--> [RETRIEVAL] Fetching relevant documentation for retry...")
        
        # Combine the error with the exact documentation needed to fix it
        full_feedback = (
            f"Fix these errors: {error_msg}\n\n"
            f"REFERENCE DOCUMENTATION:\n{docs_msg}"
        )
        
        return {
            "error_context": full_feedback,
            "retry_count": retry_count + 1
        }
        
    print("--> Code validation passed! Ready for rendering.")
    return {
        "error_context": "",
        "retry_count": retry_count 
    }