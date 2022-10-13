"""auto vote

Revision ID: 907b082cfd26
Revises: 966f58c35eba
Create Date: 2022-10-12 10:12:13.560838

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '907b082cfd26'
down_revision = '966f58c35eba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("votes",
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("links_id", sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(["links_id"], ["links.id"], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("user_id", "links_id") )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table("votes")
    # ### end Alembic commands ###
