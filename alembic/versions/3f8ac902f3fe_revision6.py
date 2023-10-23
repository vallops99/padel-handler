"""Revision6

Revision ID: 3f8ac902f3fe
Revises: 8785c1ecf946
Create Date: 2023-10-24 00:46:05.566305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f8ac902f3fe'
down_revision: Union[str, None] = '8785c1ecf946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cross_users_matches_match_id_fkey', 'cross_users_matches', type_='foreignkey')
    op.drop_constraint('cross_users_matches_user_id_fkey', 'cross_users_matches', type_='foreignkey')
    op.create_foreign_key(None, 'cross_users_matches', 'matches', ['match_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'cross_users_matches', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cross_users_matches', type_='foreignkey')
    op.drop_constraint(None, 'cross_users_matches', type_='foreignkey')
    op.create_foreign_key('cross_users_matches_user_id_fkey', 'cross_users_matches', 'users', ['user_id'], ['id'])
    op.create_foreign_key('cross_users_matches_match_id_fkey', 'cross_users_matches', 'matches', ['match_id'], ['id'])
    # ### end Alembic commands ###
