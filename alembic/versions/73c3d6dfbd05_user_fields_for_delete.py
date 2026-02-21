"""user fields for delete

Revision ID: 73c3d6dfbd05
Revises: df30aa3dee3a
Create Date: 2026-02-21 12:56:36.080742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73c3d6dfbd05'
down_revision: Union[str, Sequence[str], None] = 'df30aa3dee3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_deleted', sa.Boolean, server_default='false', nullable=False)
    )
    op.add_column(
        'users',
        sa.Column('deleted_at', sa.DateTime, nullable=True)
    )

def downgrade() -> None:
    op.drop_column('users', 'is_deleted')
    op.drop_column('users', 'deleted_at')
