"""seasons table

Revision ID: 8e998bfa515c
Revises: 9e349f8f055f
Create Date: 2025-03-15 14:16:40.842344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e998bfa515c'
down_revision: Union[str, None] = '9e349f8f055f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'seasons',
        sa.Column('season_id', sa.Integer, primary_key=True),
        sa.Column('regular_season_start_date', sa.Date),
        sa.Column('regular_season_end_date', sa.Date),
        sa.Column('playoff_end_date', sa.Date)
    )

def downgrade() -> None:
    op.drop_table('seasons')
