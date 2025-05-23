"""Add cryptography to balance account

Revision ID: 2e6eec644517
Revises: 581348ed14a9
Create Date: 2025-04-30 13:16:31.507022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from backend.crud import EncryptedBalance


# revision identifiers, used by Alembic.
revision: str = '2e6eec644517'
down_revision: Union[str, None] = '581348ed14a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('счет', sa.Column('новый_баланс', EncryptedBalance, nullable=True))

    op.drop_column('счет', 'баланс')

    op.alter_column('счет', 'новый_баланс', new_column_name='баланс')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('счет', sa.Column('старый_баланс', sa.Float, nullable=True))
    op.drop_column('счет', 'баланс')
    op.alter_column('счет', 'старый_баланс', new_column_name='баланс')
    # ### end Alembic commands ###
