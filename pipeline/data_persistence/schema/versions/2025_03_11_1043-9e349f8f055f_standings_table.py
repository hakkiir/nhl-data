"""standings table

Revision ID: 9e349f8f055f
Revises: b06d8cef3253
Create Date: 2025-03-11 10:43:14.254318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e349f8f055f'
down_revision: Union[str, None] = 'b06d8cef3253'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        'current_standings',
        sa.Column('standing_id', sa.String, primary_key=True),
        sa.Column('standings_datetime', sa.DateTime),
        sa.Column('team_id', sa.Integer, nullable=False),
        sa.Column('division_id', sa.Integer, nullable=False),
        sa.Column('conference_seq', sa.Integer, nullable=False),
        sa.Column('division_seq', sa.Integer, nullable=False),
        sa.Column('games_played', sa.Integer),
        sa.Column('goal_diff', sa.Integer),
        sa.Column('goals_against', sa.Integer),
        sa.Column('goals_for', sa.Integer),
        sa.Column('wins', sa.Integer),
        sa.Column('losses', sa.Integer),
        sa.Column('ot_losses', sa.Integer),
        sa.Column('points', sa.Integer),
        sa.Column('points_pctg', sa.Float),
        sa.Column('win_pctg', sa.Float),
        sa.Column('home_games_played', sa.Integer),
        sa.Column('home_goals_diff', sa.Integer),
        sa.Column('home_goals_against', sa.Integer),
        sa.Column('home_goals_for', sa.Integer),
        sa.Column('home_losses', sa.Integer),
        sa.Column('home_ot_losses', sa.Integer),
        sa.Column('home_points', sa.Integer),
        sa.Column('home_total_wins', sa.Integer),
        sa.Column('home_reg_wins', sa.Integer),
        sa.Column('road_games_played', sa.Integer),
        sa.Column('road_goals_diff', sa.Integer),
        sa.Column('road_goals_against', sa.Integer),
        sa.Column('road_goals_for', sa.Integer),
        sa.Column('road_losses', sa.Integer),
        sa.Column('road_ot_losses', sa.Integer),
        sa.Column('road_points', sa.Integer),
        sa.Column('road_total_wins', sa.Integer),
        sa.Column('road_reg_wins', sa.Integer),
        sa.Column('streak_code', sa.String),
        sa.Column('streak_count', sa.Integer),
        sa.Column('wildcard_seq', sa.Integer),
        sa.Column('l10_wins', sa.Integer),
        sa.Column('l10_losses', sa.Integer),
        sa.Column('l10_ot_losses', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('standings_datetime_local', sa.DateTime, sa.Computed("standings_datetime AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Helsinki'")),
        sa.ForeignKeyConstraint(['team_id'], ['public.teams.team_id']),
        sa.ForeignKeyConstraint(['division_id'], ['public.divisions.division_id'])
        )


def downgrade() -> None:
    op.drop_table('current_standings')
