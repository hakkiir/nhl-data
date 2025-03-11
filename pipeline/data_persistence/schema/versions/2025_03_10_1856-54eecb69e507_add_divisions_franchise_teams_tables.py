"""add divisions, franchise, teams tables

Revision ID: 54eecb69e507
Revises: 
Create Date: 2025-03-10 18:56:29.656565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54eecb69e507'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'divisions',
        sa.Column('division_id', sa.Integer, primary_key=True),
        sa.Column('division_name', sa.String, nullable=False, unique=True),
        sa.Column('division_abbrev', sa.String, nullable=False, unique=True),
        sa.Column('conference_name', sa.String, nullable=False, unique=False),
        sa.Column('conference_abbrev', sa.String, nullable=False, unique=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now())
    )

    op.create_table (
        'franchise',
        sa.Column('franchise_id', sa.Integer, primary_key=True, unique=True),
        sa.Column('franchise_name', sa.String(30), nullable=False),
        sa.Column('team_common_name', sa.String(20), nullable=False),
        sa.Column('team_place_name', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now())
    )

    op.create_table(
        'teams',
        sa.Column('team_id', sa.Integer, primary_key=True),
        sa.Column('franchise_id', sa.Integer, nullable=True),
        sa.Column('team_name', sa.String(30), nullable=False),
        sa.Column('league_id', sa.Integer),
        sa.Column('raw_tricode', sa.String(3)),
        sa.Column('tricode', sa.String(3)),
        sa.Column('division_id', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['franchise_id'], ['public.franchise.franchise_id']),
        sa.ForeignKeyConstraint(['division_id'], ['public.divisions.division_id'])
    )

def downgrade() -> None:
    op.drop_table('teams')
    op.drop_table('franchise')
    op.drop_table('divisions')
