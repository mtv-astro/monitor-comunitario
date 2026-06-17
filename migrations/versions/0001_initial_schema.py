"""Initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-06-17 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=160), nullable=False),
        sa.Column('phone', sa.String(length=40), nullable=False),
        sa.Column('municipality', sa.String(length=120), nullable=False),
        sa.Column('neighborhood', sa.String(length=160), nullable=False, server_default=''),
        sa.Column('street', sa.String(length=200), nullable=False, server_default=''),
        sa.Column('number', sa.String(length=40), nullable=False, server_default=''),
        sa.Column('zipcode', sa.String(length=20), nullable=False, server_default=''),
        sa.Column(
            'accept_municipality_wide_alerts',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'outage_notices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source', sa.String(length=80), nullable=False, server_default='celesc'),
        sa.Column('source_url', sa.String(length=500), nullable=False),
        sa.Column('municipality', sa.String(length=120), nullable=False),
        sa.Column('neighborhood', sa.String(length=160), nullable=False, server_default=''),
        sa.Column('street', sa.String(length=200), nullable=False, server_default=''),
        sa.Column('description', sa.Text(), nullable=False, server_default=''),
        sa.Column('raw_text', sa.Text(), nullable=False, server_default=''),
        sa.Column('content_hash', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        op.f('ix_outage_notices_municipality'),
        'outage_notices',
        ['municipality'],
        unique=False,
    )
    op.create_unique_constraint(
        'uq_outage_notices_content_hash',
        'outage_notices',
        ['content_hash'],
    )

    op.create_table(
        'monitoring_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=40), nullable=False, server_default='running'),
        sa.Column('municipalities_found', sa.Integer(), nullable=False, server_default='0'),
        sa.Column(
            'municipalities_captured',
            sa.Integer(),
            nullable=False,
            server_default='0',
        ),
        sa.Column('notices_found', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notices_persisted', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notices_created', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('users_checked', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('matches_created', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notifications_created', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error_message', sa.Text(), nullable=False, server_default=''),
        sa.Column(
            'raw_snapshot_path',
            sa.String(length=500),
            nullable=False,
            server_default='',
        ),
    )

    op.create_table(
        'user_outage_matches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('outage_notice_id', sa.Integer(), nullable=False),
        sa.Column('match_level', sa.String(length=40), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False, server_default='0'),
        sa.Column('match_reason', sa.Text(), nullable=False, server_default=''),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['outage_notice_id'], ['outage_notices.id']),
        sa.UniqueConstraint(
            'user_id',
            'outage_notice_id',
            name='uq_user_outage_match_user_notice',
        ),
    )

    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('outage_notice_id', sa.Integer(), nullable=False),
        sa.Column('channel', sa.String(length=40), nullable=False, server_default='app'),
        sa.Column('status', sa.String(length=40), nullable=False, server_default='created'),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=False, server_default=''),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['outage_notice_id'], ['outage_notices.id']),
        sa.UniqueConstraint(
            'user_id',
            'outage_notice_id',
            'channel',
            name='uq_notification_user_notice_channel',
        ),
    )

def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('user_outage_matches')
    op.drop_table('monitoring_runs')
    op.drop_index(op.f('ix_outage_notices_municipality'), table_name='outage_notices')
    op.drop_constraint('uq_outage_notices_content_hash', 'outage_notices', type_='unique')
    op.drop_table('outage_notices')
    op.drop_table('users')
