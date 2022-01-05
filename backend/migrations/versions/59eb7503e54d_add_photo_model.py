"""Add photo model

Revision ID: 59eb7503e54d
Revises: 312adc41ccaf
Create Date: 2022-01-05 16:14:05.256915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "59eb7503e54d"
down_revision = "312adc41ccaf"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "photos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("blob_path", sa.String(length=255), nullable=False),
        sa.Column(
            "model_type",
            sa.Enum("LUNG_CANCER", "PNEUMONIA", "BRAIN_TUMOUR", name="customvisionmodels"),
            nullable=False,
        ),
        sa.Column("model_result", sa.String(length=1500), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("photos")
