from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class Location(BaseModel):
    path: str
    start_line: int
    end_line: int


class Patch(Location):
    operation: Literal["replace", "insert"]
    content: Optional[str] = None


class Riew(BaseModel):
    passed: bool
    reason: Optional[str]
    
class Patches(BaseModel):
    patches: List[Patch]


class Context(BaseModel):
    issue: str = ""
    states: Patches = Field(default_factory=lambda: Patches(patches=[]))

    def update_patches(self, patches: Patches):
        self.states.patches = patches.patches


    def clear_patches(self):
        self.states.patches = []

