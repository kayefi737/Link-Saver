"""add role to users table

Revision ID: b7f3c1a9d2e4
Revises: 013d005da780
Create Date: 2026-06-22 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f3c1a9d2e4'
down_revision = '013d005da780'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(), server_default="user", nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("users", "role")
    pass
