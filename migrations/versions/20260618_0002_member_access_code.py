"""add member access code fields

Revision ID: 20260618_0002
Revises: 20260616_0001
Create Date: 2026-06-18 11:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260618_0002"
down_revision: str | None = "20260616_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "access_code_hash",
            sa.String(length=128),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "access_code_created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
    op.create_index("ix_users_phone", "users", ["phone"])


def downgrade() -> None:
    op.drop_index("ix_users_phone", table_name="users")
    op.drop_column("users", "access_code_created_at")
    op.drop_column("users", "access_code_hash")
