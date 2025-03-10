"""add players table

Revision ID: b06d8cef3253
Revises: 3d5bf9567c40
Create Date: 2025-03-10 19:04:11.444098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b06d8cef3253'
down_revision: Union[str, None] = '3d5bf9567c40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        'players',
        sa.Column('player_id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('current_team_id', sa.Integer),
        sa.Column('sweater_number', sa.Integer),
        sa.Column('position_code', sa.String(10)),
        sa.Column('shoots_catches', sa.String(10)),
        sa.Column('height_in_cm', sa.Integer),
        sa.Column('weight_in_kg', sa.Integer),
        sa.Column('birth_date', sa.Date),
        sa.Column('birth_city', sa.String(50)),
        sa.Column('birth_country', sa.String(50)),
        sa.Column('birth_state_province', sa.String(20)),
        sa.Column('headshot_url', sa.String(100)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['current_team_id'], ['public.teams.team_id'])
        )

def downgrade() -> None:
    op.drop_table('players')