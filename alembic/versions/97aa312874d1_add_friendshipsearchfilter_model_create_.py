"""Add FriendshipSearchFilter model, create GenderEnum

Revision ID: 97aa312874d1
Revises: 2d6021a0c98b
Create Date: 2024-11-14 00:32:46.420134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '97aa312874d1'
down_revision: Union[str, None] = '2d6021a0c98b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friendships_search_filter',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('region', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('search_id_list', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('city_search', sa.Boolean(), nullable=False),
    sa.Column('gender', sa.Enum('MAN', 'WOMAN', 'BOTH', 'OTHER', name='gender_enum'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_friendships_search_filter_user_id'), 'friendships_search_filter', ['user_id'], unique=False)
    op.add_column('bios', sa.Column('gender', sa.Enum('MAN', 'WOMAN', 'BOTH', 'OTHER', name='gender_enum'), nullable=False))
    op.drop_column('bios', 'beyond_city_search_id')
    op.drop_column('bios', 'city_search')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bios', sa.Column('city_search', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('bios', sa.Column('beyond_city_search_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('bios', 'gender')
    op.drop_index(op.f('ix_friendships_search_filter_user_id'), table_name='friendships_search_filter')
    op.drop_table('friendships_search_filter')
    # ### end Alembic commands ###
