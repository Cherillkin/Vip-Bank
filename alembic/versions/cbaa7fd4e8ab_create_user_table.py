"""Create User table

Revision ID: cbaa7fd4e8ab
Revises: 
Create Date: 2025-04-15 17:52:48.477621
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'cbaa7fd4e8ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create the 'роли' table
    op.create_table(
        'роли',
        sa.Column('id_роли', sa.Integer, primary_key=True),
        sa.Column('роль', sa.String, unique=True, nullable=False)
    )

    # Create the 'клиент' table
    op.create_table(
        'клиент',
        sa.Column('id_клиента', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('фамилия', sa.String),
        sa.Column('имя', sa.String),
        sa.Column('отчество', sa.String),
        sa.Column('дата_создания', sa.DateTime, default=sa.func.now()),
        sa.Column('дата_обновление', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('пароль', sa.String),
        sa.Column('id_роли', sa.Integer, sa.ForeignKey('роли.id_роли'))
    )

    # Create the 'филиал' table
    op.create_table(
        'филиал',
        sa.Column('id_филиала', sa.Integer, primary_key=True),
        sa.Column('улица_филиала', sa.Integer, sa.ForeignKey('улица.id_улицы')),
        sa.Column('дом_филиала', sa.Integer),
        sa.Column('корпус_филиала', sa.Integer)
    )

    # Create the 'улица' table
    op.create_table(
        'улица',
        sa.Column('id_улицы', sa.Integer, primary_key=True),
        sa.Column('название_улицы', sa.String)
    )

    # Create the 'счет' table
    op.create_table(
        'счет',
        sa.Column('id_счета', sa.Integer, primary_key=True),
        sa.Column('баланс', sa.Integer),
        sa.Column('id_клиента', sa.Integer, sa.ForeignKey('клиент.id_клиента')),
        sa.Column('id_филиала', sa.Integer, sa.ForeignKey('филиал.id_филиала')),
        sa.Column('дата_открытия', sa.DateTime, default=sa.func.now())
    )

    # Create the 'вид_счета' table
    op.create_table(
        'вид_счета',
        sa.Column('id_вида_счета', sa.Integer, primary_key=True),
        sa.Column('название_вида_счета', sa.String)
    )

    # Create the 'тип_счета' table
    op.create_table(
        'тип_счета',
        sa.Column('id_типа_счета', sa.Integer, primary_key=True),
        sa.Column('название_типа_счета', sa.String)
    )

    # Create the 'процентная_ставка_в_сч' table
    op.create_table(
        'процентная_ставка_в_сч',
        sa.Column('id_процентной_ставки', sa.Integer, primary_key=True),
        sa.Column('процентная_ставка', sa.Integer),
        sa.Column('id_вида_счета', sa.Integer, sa.ForeignKey('вид_счета.id_вида_счета')),
        sa.Column('дата_изменения', sa.DateTime, default=sa.func.now())
    )

    # Create the 'банковская_операция' table
    op.create_table(
        'банковская_операция',
        sa.Column('id_банковской_операции', sa.Integer, primary_key=True),
        sa.Column('id_счета', sa.Integer, sa.ForeignKey('счет.id_счета')),
        sa.Column('сумма', sa.Integer),
        sa.Column('id_операции', sa.Integer, sa.ForeignKey('операции.id_операции'))
    )

    # Create the 'операции' table
    op.create_table(
        'операции',
        sa.Column('id_операции', sa.Integer, primary_key=True),
        sa.Column('название_операции', sa.String)
    )

    # Create the 'инвестиции' table
    op.create_table(
        'инвестиции',
        sa.Column('id_портфеля', sa.Integer, primary_key=True),
        sa.Column('id_клиента', sa.Integer, sa.ForeignKey('клиент.id_клиента')),
        sa.Column('баланс', sa.Integer),
        sa.Column('дата_создания', sa.DateTime, default=sa.func.now()),
        sa.Column('статус', sa.String)
    )

    # Create the 'типы_инвестиций' table
    op.create_table(
        'типы_инвестиций',
        sa.Column('id_типа_инвестиций', sa.Integer, primary_key=True),
        sa.Column('название_типа', sa.String)
    )

    # Create the 'детали_инвестиций' table
    op.create_table(
        'детали_инвестиций',
        sa.Column('id_детали', sa.Integer, primary_key=True),
        sa.Column('id_портфеля', sa.Integer, sa.ForeignKey('инвестиции.id_портфеля')),
        sa.Column('id_типа_инвестиций', sa.Integer, sa.ForeignKey('типы_инвестиций.id_типа_инвестиций')),
        sa.Column('сумма', sa.Integer),
        sa.Column('дата_покупки', sa.DateTime, default=sa.func.now())
    )

    # Create the 'доходность_инвестиций' table
    op.create_table(
        'доходность_инвестиций',
        sa.Column('id_доходности', sa.Integer, primary_key=True),
        sa.Column('id_портфеля', sa.Integer, sa.ForeignKey('инвестиции.id_портфеля')),
        sa.Column('доходность', sa.Float),
        sa.Column('дата_обновления', sa.DateTime, default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('доходность_инвестиций')
    op.drop_table('детали_инвестиций')
    op.drop_table('типы_инвестиций')
    op.drop_table('инвестиции')
    op.drop_table('операции')
    op.drop_table('банковская_операция')
    op.drop_table('процентная_ставка_в_сч')
    op.drop_table('тип_счета')
    op.drop_table('вид_счета')
    op.drop_table('счет')
    op.drop_table('филиал')
    op.drop_table('улица')
    op.drop_table('клиент')
    op.drop_table('роли')
