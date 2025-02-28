"""create franchises table

Revision ID: d47dd3e6a3f0
Revises: 
Create Date: 2025-02-25 10:41:08.402839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd47dd3e6a3f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'franchise',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('fullName', sa.String(30), nullable=False),
        sa.Column('teamCommonName', sa.String(20), nullable=False),
        sa.Column('teamPlaceName', sa.String(20), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('franchise')
