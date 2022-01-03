"""Add user model

Revision ID: 56b064319558
Revises: 
Create Date: 2022-01-03 21:08:09.721884

"""
from alembic import op
import sqlalchemy as sa


revision = "6b064319558"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("users")
