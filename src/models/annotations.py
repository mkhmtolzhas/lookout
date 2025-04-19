from sqlalchemy import text
from sqlalchemy.orm import mapped_column
from typing import Annotated
from datetime import datetime


IDPK = Annotated[int, mapped_column(primary_key=True, index=True)]
CreatedAt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE(('utc'), now())"))]
UpdatedAt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE(('utc'), now())"), onupdate=text("TIMEZONE(('utc'), now())"))]