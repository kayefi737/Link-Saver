"""add links table

Revision ID: 7a6b748c869d
Revises: c709a8c62068
Create Date: 2022-10-11 13:18:56.307165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a6b748c869d'
down_revision = 'c709a8c62068'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("links", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title",sa.String(),nullable=False), sa.Column("content", sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("links")
    pass
