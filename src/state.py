from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class VideoIntent(BaseModel):
    """Structured output from the Prompt Parser."""
    pacing: str = Field(description="The pacing of the video (e.g., fast, slow, dynamic)")
    visual_style: str = Field(description="The visual style treatment (e.g., cinematic, upbeat)")
    caption_tone: str = Field(description="The tone of the captions")
    transition_preference: str = Field(description="The preferred transitions between images")

class GraphState(TypedDict):
    """The shared state object that all nodes will read from and write to."""
    user_prompt: str
    intent: Optional[VideoIntent]
    selected_images: List[str]
    storyboard: dict
    remotion_script: str
    error_context: str
    retry_count: int