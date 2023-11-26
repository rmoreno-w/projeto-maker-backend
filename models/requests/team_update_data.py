from typing import Optional

from pydantic import BaseModel


class TeamUpdateData(BaseModel):
    area: Optional[str] = None
    description: Optional[str] = None