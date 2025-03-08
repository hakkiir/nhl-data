"""create teams table

Revision ID: 02419f4f67df
Revises: d47dd3e6a3f0
Create Date: 2025-02-28 15:31:27.652103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02419f4f67df'
down_revision: Union[str, None] = 'd47dd3e6a3f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        'teams',
        sa.Column('team_id', sa.Integer, primary_key=True),
        sa.Column('franchise_id', sa.Integer, nullable=True),
        sa.Column('full_name', sa.String(30), nullable=False),
        sa.Column('league_id', sa.Integer),
        sa.Column('raw_tricode', sa.String(3)),
        sa.Column('tricode', sa.String(3)),
        sa.ForeignKeyConstraint(['franchise_id'], ['public.franchise.franchise_id']),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('teams')
