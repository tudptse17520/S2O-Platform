"""Add created_at to promotions and create payments table

Revision ID: add_promotions_payments
Revises: e57f6af8821f
Create Date: 2026-01-29 04:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_promotions_payments'
down_revision: Union[str, Sequence[str], None] = 'e57f6af8821f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add missing columns and tables."""
    # Add created_at and updated_at to promotions if not exists
    try:
        op.add_column('promotions', sa.Column('created_at', sa.DateTime(), nullable=True))
        op.add_column('promotions', sa.Column('updated_at', sa.DateTime(), nullable=True))
    except Exception:
        pass  # Columns may already exist
    
    # Create payments table if not exists
    op.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            tenant_id UUID NOT NULL REFERENCES tenants(id),
            order_id UUID NOT NULL REFERENCES orders(id),
            amount FLOAT NOT NULL,
            method VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            transaction_id VARCHAR(255),
            id UUID NOT NULL PRIMARY KEY,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)


def downgrade() -> None:
    """Revert changes."""
    op.execute("DROP TABLE IF EXISTS payments")
    try:
        op.drop_column('promotions', 'created_at')
        op.drop_column('promotions', 'updated_at')
    except Exception:
        pass
