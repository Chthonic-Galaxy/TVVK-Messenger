"""add public_key to users table

Revision ID: c843abc6a599
Revises: b8a54f81fdab
Create Date: 2025-01-20 12:32:19.505503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c843abc6a599'
down_revision: Union[str, None] = 'b8a54f81fdab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('public_key', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'public_key')
    # ### end Alembic commands ###
