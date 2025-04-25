"""Search result models."""

from typing import Optional
from pydantic import BaseModel


class SearchResult(BaseModel):
    """Search result model."""

    score: float
    text: str
    source_type: str
    source_title: str
    source_url: Optional[str] = None
    file_path: Optional[str] = None
    repo_name: Optional[str] = None
