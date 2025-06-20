"""Add index to Cita.creado_en

Revision ID: 92f9a2d4d89b
Revises: b2f9a1c4d567
Create Date: 2025-06-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '92f9a2d4d89b'
down_revision = 'b2f9a1c4d567'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_citas_creado_en', 'citas', ['creado_en'])


def downgrade():
    op.drop_index('ix_citas_creado_en', table_name='citas')
