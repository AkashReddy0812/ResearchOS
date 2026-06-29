from typing import Optional

from pydantic import BaseModel


class Document(BaseModel):
    """
    Represents a downloaded research document.
    """

    paper_id: str

    title: str

    file_path: str

    source_url: str

    pages: Optional[int] = None