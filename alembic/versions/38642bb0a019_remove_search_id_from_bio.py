"""Remove search id from Bio

Revision ID: 38642bb0a019
Revises: 97aa312874d1
Create Date: 2024-11-14 00:41:41.787897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38642bb0a019'
down_revision: Union[str, None] = '97aa312874d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bios', 'search_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bios', sa.Column('search_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
