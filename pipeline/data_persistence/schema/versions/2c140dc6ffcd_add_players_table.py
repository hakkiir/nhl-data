"""add players table

Revision ID: 2c140dc6ffcd
Revises: f879b710bd2a
Create Date: 2025-03-04 17:09:04.649661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c140dc6ffcd'
down_revision: Union[str, None] = 'f879b710bd2a'
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
        sa.ForeignKeyConstraint(['current_team_id'], ['public.teams.team_id'])
        )

def downgrade() -> None:
    pass

'''
        {
            "id": 8480980,
            "headshot": "https://assets.nhle.com/mugs/nhl/20242025/TOR/8480980.png",
            "firstName": {
                "default": "Connor"
            },
            "lastName": {
                "default": "Dewar"
            },
            "sweaterNumber": 24,
            "positionCode": "C",
            "shootsCatches": "L",
            "heightInInches": 70,
            "weightInPounds": 192,
            "heightInCentimeters": 178,
            "weightInKilograms": 87,
            "birthDate": "1999-06-26",
            "birthCity": {
                "default": "The Pas"
            },
            "birthCountry": "CAN",
            "birthStateProvince": {
                "default": "MB"
            }
        }
'''