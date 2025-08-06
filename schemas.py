from typing import List, Optional
from pydantic import BaseModel

class SingulApp(BaseModel):
    """Schema for a single Singul app"""
    name: str
    description: str
    categories: List[str]
    action_labels: List[str]
    tags: List[str]
    actions_count: int
    verified: bool

class SingulAppSearchResult(BaseModel):
    """Schema for search results"""
    query: str
    total_hits: int
    apps: List[SingulApp]
    error: Optional[str] = None