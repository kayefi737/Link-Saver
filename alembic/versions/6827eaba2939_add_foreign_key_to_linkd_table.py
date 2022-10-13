"""add foreign key to linkd table

Revision ID: 6827eaba2939
Revises: c429decab17a
Create Date: 2022-10-11 13:26:10.427433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6827eaba2939'
down_revision = 'c429decab17a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("links", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("links_users_fk", source_table= "links",referent_table="users",
                        local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("links_users_fk", table_name="links")
    op.drop_column("links", "owner_id")
    pass
