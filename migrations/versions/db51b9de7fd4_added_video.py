"""added video

Revision ID: db51b9de7fd4
Revises: a87d64249ff7
Create Date: 2025-04-20 01:13:21.404230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db51b9de7fd4'
down_revision: Union[str, None] = 'a87d64249ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
