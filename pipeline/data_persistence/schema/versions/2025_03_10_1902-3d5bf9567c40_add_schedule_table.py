"""add schedule table

Revision ID: 3d5bf9567c40
Revises: 54eecb69e507
Create Date: 2025-03-10 19:02:32.674251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d5bf9567c40'
down_revision: Union[str, None] = '54eecb69e507'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'schedule',
        sa.Column('game_id', sa.Integer, primary_key=True),
        sa.Column('season', sa.Integer, nullable=False),
        sa.Column('game_type', sa.Integer),
        sa.Column('neutral_site', sa.Boolean),
        sa.Column('starttime_utc', sa.DateTime, nullable=False),
        sa.Column('game_state', sa.String(10)),
        sa.Column('away_team_id', sa.Integer, nullable=False),
        sa.Column('away_team_score', sa.Integer),
        sa.Column('home_team_id', sa.Integer, nullable=False),
        sa.Column('home_team_score', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['away_team_id'], ['public.teams.team_id']),
        sa.ForeignKeyConstraint(['home_team_id'], ['public.teams.team_id'])
    )

def downgrade() -> None:
    op.drop_table('schedule')
