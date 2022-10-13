"""add is_active to users table

Revision ID: 013d005da780
Revises: 0baa852b3d0f
Create Date: 2022-10-12 15:33:25.782099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '013d005da780'
down_revision = '0baa852b3d0f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_active", sa.Boolean(), server_default="False"))  
    pass


def downgrade() -> None:
    op.drop_column("users", "is_active")
    pass
