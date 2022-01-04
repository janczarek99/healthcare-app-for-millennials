"""Add document model

Revision ID: 312adc41ccaf
Revises: 6b064319558
Create Date: 2022-01-04 22:01:25.787414

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "312adc41ccaf"
down_revision = "6b064319558"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("blob_path", sa.String(length=255), nullable=False),
        sa.Column("ocred_text", sa.String(length=10000), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("documents")
