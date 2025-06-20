"""Add indexes to frequently filtered columns

Revision ID: b2f9a1c4d567
Revises: 3f4319747613
Create Date: 2025-06-20 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b2f9a1c4d567'
down_revision = '3f4319747613'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_sms_estado', 'sms', ['estado'])
    op.create_index('ix_sms_fecha_envio', 'sms', ['fecha_envio'])
    op.create_index('ix_citas_fecha_hora', 'citas', ['fecha_hora'])
    op.create_index('ix_pacientes_programada', 'pacientes', ['programada'])
    op.create_index('ix_confirmaciones_confirmada_en', 'confirmaciones', ['confirmada_en'])
    op.create_index('ix_sms_pendientes_fecha_programada', 'sms_pendientes', ['fecha_programada'])
    op.create_index('ix_sms_pendientes_estado', 'sms_pendientes', ['estado'])


def downgrade():
    op.drop_index('ix_sms_pendientes_estado', table_name='sms_pendientes')
    op.drop_index('ix_sms_pendientes_fecha_programada', table_name='sms_pendientes')
    op.drop_index('ix_confirmaciones_confirmada_en', table_name='confirmaciones')
    op.drop_index('ix_pacientes_programada', table_name='pacientes')
    op.drop_index('ix_citas_fecha_hora', table_name='citas')
    op.drop_index('ix_sms_fecha_envio', table_name='sms')
    op.drop_index('ix_sms_estado', table_name='sms')
