"""Add Bio model

Revision ID: edbca894a74a
Revises: 01240e283e88
Create Date: 2024-11-13 10:34:37.289272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edbca894a74a'
down_revision: Union[str, None] = '01240e283e88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('profile_name', sa.String(length=50), nullable=False),
    sa.Column('profile_bio', sa.String(length=255), nullable=False),
    sa.Column('profile_age', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.String(length=15), nullable=False),
    sa.Column('longitude', sa.String(length=15), nullable=False),
    sa.Column('profile_city', sa.String(length=50), nullable=False),
    sa.Column('search_id', sa.Integer(), nullable=False),
    sa.Column('beyond_city_search_id', sa.Integer(), nullable=False),
    sa.Column('city_search', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bios_user_id'), 'bios', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bios_user_id'), table_name='bios')
    op.drop_table('bios')
    # ### end Alembic commands ###
