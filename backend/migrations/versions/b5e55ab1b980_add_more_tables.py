from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = 'b5e55ab1b980'
down_revision = 'f12dc534ada3'
branch_labels = None
depends_on = None

def upgrade():
    # Vérification et création de la table 'site'
    conn = op.get_bind()
    result = conn.execute("SHOW TABLES LIKE 'site'")
    if not result.fetchone():
        op.create_table('site',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('nom', sa.String(length=50), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )

    # Vérification et création de la table 'promotion'
    result = conn.execute("SHOW TABLES LIKE 'promotion'")
    if not result.fetchone():
        op.create_table('promotion',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('nom', sa.String(length=50), nullable=False),
            sa.Column('site_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['site_id'], ['site.id']),
            sa.PrimaryKeyConstraint('id')
        )

    # Vérification et création de la table 'groupe'
    result = conn.execute("SHOW TABLES LIKE 'groupe'")
    if not result.fetchone():
        op.create_table('groupe',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('nom', sa.String(length=50), nullable=False),
            sa.Column('promotion_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['promotion_id'], ['promotion.id']),
            sa.PrimaryKeyConstraint('id')
        )

    # Vérification de l'existence de la colonne 'promotion_id' avant de l'ajouter
    result = conn.execute("SHOW COLUMNS FROM etudiant LIKE 'promotion_id'")
    if not result.fetchone():
        with op.batch_alter_table('etudiant', schema=None) as batch_op:
            batch_op.add_column(sa.Column('promotion_id', sa.Integer(), nullable=False))
            batch_op.add_column(sa.Column('groupe_id', sa.Integer(), nullable=False))
            batch_op.add_column(sa.Column('site_id', sa.Integer(), nullable=False))
            batch_op.create_unique_constraint(None, ['email'])
            batch_op.create_foreign_key(None, 'promotion', ['promotion_id'], ['id'])
            batch_op.create_foreign_key(None, 'site', ['site_id'], ['id'])
            batch_op.create_foreign_key(None, 'groupe', ['groupe_id'], ['id'])
            batch_op.drop_column('promotion')
            batch_op.drop_column('site')
            batch_op.drop_column('groupe')


def downgrade():
    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('groupe', mysql.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('site', mysql.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('promotion', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('site_id')
        batch_op.drop_column('groupe_id')
        batch_op.drop_column('promotion_id')

    op.drop_table('groupe')
    op.drop_table('promotion')
    op.drop_table('site')
