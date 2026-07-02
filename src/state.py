from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from typing import List

class VideoIntent(BaseModel):
    """Structured output from the Prompt Parser."""
    pacing: str = Field(description="The pacing of the video (e.g., fast, slow, dynamic)")
    visual_style: str = Field(description="The visual style treatment (e.g., cinematic, upbeat)")
    caption_tone: str = Field(description="The tone of the captions")
    transition_preference: str = Field(description="The preferred transitions between images")

class RemotionScript(BaseModel):
    code: str = Field(description="The fully runnable React/Remotion code string")

class GraphState(TypedDict):
    """The shared state object that all nodes will read from and write to."""
    user_prompt: str
    intent: Optional[VideoIntent]
    selected_images: List[str]
    storyboard: dict
    remotion_script: str
    error_context: str
    retry_count: int

# --- Phase 3 Pydantic Models ---

class Scene(BaseModel):
    image_filename: str = Field(description="The filename of the selected image")
    caption: str = Field(description="The text overlay for this scene")
    duration_in_frames: int = Field(description="How long this scene lasts")
    transition_style: str = Field(description="How to transition to the next scene")

class Storyboard(BaseModel):
    scenes: List[Scene] = Field(description="The chronological sequence of scenes")
