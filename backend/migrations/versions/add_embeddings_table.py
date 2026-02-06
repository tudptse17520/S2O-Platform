"""Add embeddings table for vector search

Revision ID: add_embeddings_table
Revises: add_promotions_payments
Create Date: 2026-02-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = 'add_embeddings_table'
down_revision = 'add_promotions_payments'
branch_labels = None
depends_on = None


def upgrade():
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create embeddings table
    op.create_table(
        'embeddings',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=True),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('embedding', sa.String, nullable=True),  # Will store vector as string, pgvector handles conversion
        sa.Column('metadata', sa.Text, nullable=True),
        sa.Column('entity_type', sa.String(50), nullable=True),  # e.g., 'product', 'restaurant', 'review'
        sa.Column('entity_id', sa.String(255), nullable=True),  # Reference to the entity
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Create index for vector similarity search
    # Note: This assumes pgvector extension is installed
    # For production, you may want to use IVFFlat or HNSW index
    op.execute('''
        DO $$
        BEGIN
            -- Add vector column if pgvector is available
            BEGIN
                ALTER TABLE embeddings ADD COLUMN embedding_vector vector(1536);
            EXCEPTION WHEN undefined_object THEN
                RAISE NOTICE 'vector type not available, skipping embedding_vector column';
            END;
            
            -- Create index on vector column if it exists
            BEGIN
                CREATE INDEX IF NOT EXISTS idx_embeddings_vector 
                ON embeddings USING ivfflat (embedding_vector vector_cosine_ops)
                WITH (lists = 100);
            EXCEPTION WHEN undefined_column THEN
                RAISE NOTICE 'embedding_vector column not found, skipping index';
            END;
        END $$;
    ''')
    
    # Create indexes for lookup
    op.create_index('idx_embeddings_tenant', 'embeddings', ['tenant_id'])
    op.create_index('idx_embeddings_entity', 'embeddings', ['entity_type', 'entity_id'])


def downgrade():
    op.drop_index('idx_embeddings_entity', 'embeddings')
    op.drop_index('idx_embeddings_tenant', 'embeddings')
    op.drop_table('embeddings')
