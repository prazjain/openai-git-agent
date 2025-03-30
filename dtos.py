from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Optional
@dataclass
class CodeTask(BaseModel):
    """Schema for code solution"""
    code: str = Field(..., title="Code solution")
    task_description: str = Field(..., title="Description of task")

@dataclass
class CodeSolution(BaseModel):
    """Schema for code solution"""
    code: str = Field(..., title="Code solution")
    description: str = Field(..., title="Description of the code solution")

@dataclass
class CodeFeedback(BaseModel):
    feedback: str = Field(..., title="Feedback on code solution")
    refine_further: bool = Field(..., title="Flag to determine if code solution needs further refinement")
