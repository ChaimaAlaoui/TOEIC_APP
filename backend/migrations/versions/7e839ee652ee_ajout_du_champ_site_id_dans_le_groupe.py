"""Ajout du champ site_id dans le groupe

Revision ID: 7e839ee652ee
Revises: b5e55ab1b980
Create Date: 2025-02-08 20:48:09.342642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e839ee652ee'
down_revision = 'b5e55ab1b980'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'promotion', ['promotion_id'], ['id'])
        batch_op.create_foreign_key(None, 'groupe', ['groupe_id'], ['id'])
        batch_op.create_foreign_key(None, 'site', ['site_id'], ['id'])

    with op.batch_alter_table('groupe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('site_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'site', ['site_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groupe', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('site_id')

    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
