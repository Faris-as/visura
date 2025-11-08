"""add role enum and convert is_admin

Revision ID: ab37d763f770
Revises: 88a448614cbb
Create Date: 2025-11-08 12:20:00.788104+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ab37d763f770'
down_revision: Union[str, None] = '88a448614cbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = postgresql.ENUM('user', 'admin', 'developer', name='roleenum')
    role_enum.create(op.get_bind(), checkfirst=True)
    
    op.add_column('login', sa.Column('role', sa.Enum('user', 'admin', 'developer', name='roleenum'), nullable=True, server_default='user'))

    conn = op.get_bind()
    conn.execute(sa.text("UPDATE login SET role = 'admin' WHERE is_admin = true;"))

    op.alter_column('login', 'role', nullable=False)

    op.drop_column('login', 'is_admin')


def downgrade() -> None:
    op.add_column('login', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE login SET is_admin = true WHERE role = 'admin';"))
    op.alter_column('login', 'is_admin', nullable=False)
    op.drop_column('login', 'role')
    role_enum = postgresql.ENUM('user','admin','developer', name='roleenum')
    role_enum.drop(op.get_bind(), checkfirst=True)