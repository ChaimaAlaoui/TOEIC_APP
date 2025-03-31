"""Ajout de l'email à Etudiant

Revision ID: f12dc534ada3
Revises: 2c0ec2364d2e
Create Date: 2025-01-31 13:36:21.396761

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'f12dc534ada3'
down_revision = '2c0ec2364d2e'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the 'email' column already exists
    connection = op.get_bind()
    inspector = inspect(connection)
    columns = inspector.get_columns('etudiant')
    column_names = [column['name'] for column in columns]

    # Only add the 'email' column if it doesn't already exist
    if 'email' not in column_names:
        with op.batch_alter_table('etudiant', schema=None) as batch_op:
            batch_op.add_column(sa.Column('email', sa.String(length=150), nullable=False))
            batch_op.create_unique_constraint('uq_email', ['email'])

    # Add the new columns 'site' and 'specialite'
    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('site', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('specialite', sa.String(length=100), nullable=False))


def downgrade():
    # Remove the 'site' and 'specialite' columns
    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.drop_column('site')
        batch_op.drop_column('specialite')

    # Optionally, remove the 'email' column if it was added by this migration
    connection = op.get_bind()
    inspector = inspect(connection)
    columns = inspector.get_columns('etudiant')
    column_names = [column['name'] for column in columns]

    if 'email' in column_names:
        with op.batch_alter_table('etudiant', schema=None) as batch_op:
            batch_op.drop_constraint('uq_email', type_='unique')
            batch_op.drop_column('email')