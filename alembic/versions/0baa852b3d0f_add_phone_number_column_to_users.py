"""add phone_number column to users

Revision ID: 0baa852b3d0f
Revises: 907b082cfd26
Create Date: 2022-10-12 10:35:44.975452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0baa852b3d0f'
down_revision = '907b082cfd26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String()))
    pass


def downgrade() -> None:
    op.drop_column("users", "phone_number")
    pass
