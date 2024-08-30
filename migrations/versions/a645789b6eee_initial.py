from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'a645789b6eee'
down_revision = '0ad4b30ee486'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # `USING` klauzulasini qo'shib ustunni `INTEGER` ga o'zgartirish
    op.alter_column('school_data', 'school_number',
                    type_=sa.Integer(),
                    existing_type=sa.String(),
                    existing_type_length=255,
                    postgresql_using='school_number::integer')

def downgrade() -> None:
    # Agar kerak bo'lsa, `INTEGER` dan `TEXT` ga qaytarish
    op.alter_column('school_data', 'school_number',
                    type_=sa.String(),
                    existing_type=sa.Integer(),
                    postgresql_using='school_number::text')
