"""add divisions table

Revision ID: 018ce256141a
Revises: 2c140dc6ffcd
Create Date: 2025-03-07 10:19:07.417124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '018ce256141a'
down_revision: Union[str, None] = '2c140dc6ffcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'divisions',
        sa.Column('division_id', sa.Integer, autoincrement=True, primary_key=True, unique=True),
        sa.Column('division_name', sa.String, nullable=False, unique=True),
        sa.Column('division_abbrev', sa.String, nullable=False, unique=True),
        sa.Column('conference_name', sa.String, nullable=False, unique=False),
        sa.Column('conference_abbrev', sa.String, nullable=False, unique=False)
    )

def downgrade() -> None:
    op.drop_table('divisions')