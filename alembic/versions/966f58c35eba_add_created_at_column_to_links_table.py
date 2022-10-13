"""add created_at column to links table

Revision ID: 966f58c35eba
Revises: 6827eaba2939
Create Date: 2022-10-12 03:35:58.989944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '966f58c35eba'
down_revision = '6827eaba2939'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("links", sa.Column("created_at", sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),
                            nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("links","created_at")
    pass
