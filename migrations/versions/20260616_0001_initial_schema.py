"""initial schema

Revision ID: 20260616_0001
Revises:
Create Date: 2026-06-16 22:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260616_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=False),
        sa.Column("municipality", sa.String(length=120), nullable=False),
        sa.Column("neighborhood", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("street", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("number", sa.String(length=40), nullable=False, server_default=""),
        sa.Column("zipcode", sa.String(length=20), nullable=False, server_default=""),
        sa.Column(
            "accept_municipality_wide_alerts",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "outage_notices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=80), nullable=False, server_default="celesc"),
        sa.Column("source_url", sa.String(length=500), nullable=False),
        sa.Column("municipality", sa.String(length=120), nullable=False),
        sa.Column("neighborhood", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("street", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("raw_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_outage_notices_municipality", "outage_notices", ["municipality"])
    op.create_index(
        "ix_outage_notices_content_hash",
        "outage_notices",
        ["content_hash"],
        unique=True,
    )

    op.create_table(
        "user_outage_matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "outage_notice_id",
            sa.Integer(),
            sa.ForeignKey("outage_notices.id"),
            nullable=False,
        ),
        sa.Column("match_level", sa.String(length=40), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("match_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "user_id",
            "outage_notice_id",
            name="uq_user_outage_match_user_notice",
        ),
    )
    op.create_index("ix_user_outage_matches_user_id", "user_outage_matches", ["user_id"])
    op.create_index(
        "ix_user_outage_matches_outage_notice_id",
        "user_outage_matches",
        ["outage_notice_id"],
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "outage_notice_id",
            sa.Integer(),
            sa.ForeignKey("outage_notices.id"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(length=40), nullable=False, server_default="app"),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="created"),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "user_id",
            "outage_notice_id",
            "channel",
            name="uq_notification_user_notice_channel",
        ),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_notifications_outage_notice_id", "notifications", ["outage_notice_id"])

    op.create_table(
        "monitoring_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="running"),
        sa.Column("municipalities_found", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("municipalities_captured", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notices_found", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notices_persisted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notices_created", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("users_checked", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("matches_created", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notifications_created", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=False, server_default=""),
        sa.Column("raw_snapshot_path", sa.String(length=500), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_table("monitoring_runs")

    op.drop_index("ix_notifications_outage_notice_id", table_name="notifications")
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")

    op.drop_index("ix_user_outage_matches_outage_notice_id", table_name="user_outage_matches")
    op.drop_index("ix_user_outage_matches_user_id", table_name="user_outage_matches")
    op.drop_table("user_outage_matches")

    op.drop_index("ix_outage_notices_content_hash", table_name="outage_notices")
    op.drop_index("ix_outage_notices_municipality", table_name="outage_notices")
    op.drop_table("outage_notices")

    op.drop_table("users")
