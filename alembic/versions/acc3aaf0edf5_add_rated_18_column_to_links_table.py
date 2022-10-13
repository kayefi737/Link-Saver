"""add rated_18 column to links table

Revision ID: acc3aaf0edf5
Revises: 7a6b748c869d
Create Date: 2022-10-11 13:21:50.600706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acc3aaf0edf5'
down_revision = '7a6b748c869d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("links", sa.Column("rated_18",sa.Boolean(), server_default="False", nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("links","rated_18")
    pass
