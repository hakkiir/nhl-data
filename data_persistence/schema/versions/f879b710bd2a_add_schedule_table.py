"""add schedule table

Revision ID: f879b710bd2a
Revises: 02419f4f67df
Create Date: 2025-03-04 11:44:22.605253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f879b710bd2a'
down_revision: Union[str, None] = '02419f4f67df'
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
        sa.Column('winning_goalie_id', sa.Integer),
        sa.Column('winning_goal_scorer_id', sa.Integer),
        sa.ForeignKeyConstraint(['away_team_id'], ['public.teams.team_id']),
        sa.ForeignKeyConstraint(['home_team_id'], ['public.teams.team_id']),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('schedule')
