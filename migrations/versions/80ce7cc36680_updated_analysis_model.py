"""updated analysis model

Revision ID: 80ce7cc36680
Revises: 05fdf0d59c7c
Create Date: 2025-04-27 14:36:56.872038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80ce7cc36680'
down_revision: Union[str, None] = '05fdf0d59c7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
