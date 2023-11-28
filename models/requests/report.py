from datetime import datetime

from pydantic import BaseModel


class ReportData(BaseModel):
    initial_date: str
    final_date:  str