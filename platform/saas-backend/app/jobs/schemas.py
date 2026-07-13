from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class JobSubmitResponse(BaseModel):
    job_id: str
    status: str
    product_slug: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    product_slug: str
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[Any] = None
    error_message: Optional[str] = None
