"""create contacts table

Revision ID: b8a54f81fdab
Revises: d9130cc333d3
Create Date: 2025-01-15 12:51:56.735053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8a54f81fdab'
down_revision: Union[str, None] = 'd9130cc333d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_id'), 'contacts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contacts_id'), table_name='contacts')
    op.drop_table('contacts')
    # ### end Alembic commands ###
