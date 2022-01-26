"""first commit

Revision ID: 739b75b0b4fe
Revises: 
Create Date: 2022-01-25 09:14:30.888020

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '739b75b0b4fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commerce',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=50), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('api_key', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_commerce_id'), 'commerce', ['id'], unique=False)
    op.create_index(op.f('ix_commerce_name'), 'commerce', ['name'], unique=False)
    op.create_index(op.f('ix_commerce_phone'), 'commerce', ['phone'], unique=True)
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=40), nullable=True),
    sa.Column('pin', sa.String(length=6), nullable=True),
    sa.Column('commerce_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['commerce_id'], ['commerce.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pin', 'commerce_id', name='_pin_commerce_uc')
    )
    op.create_index(op.f('ix_employee_id'), 'employee', ['id'], unique=False)
    op.create_index(op.f('ix_employee_last_name'), 'employee', ['last_name'], unique=False)
    op.create_index(op.f('ix_employee_name'), 'employee', ['name'], unique=False)
    op.create_index(op.f('ix_employee_pin'), 'employee', ['pin'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employee_pin'), table_name='employee')
    op.drop_index(op.f('ix_employee_name'), table_name='employee')
    op.drop_index(op.f('ix_employee_last_name'), table_name='employee')
    op.drop_index(op.f('ix_employee_id'), table_name='employee')
    op.drop_table('employee')
    op.drop_index(op.f('ix_commerce_phone'), table_name='commerce')
    op.drop_index(op.f('ix_commerce_name'), table_name='commerce')
    op.drop_index(op.f('ix_commerce_id'), table_name='commerce')
    op.drop_table('commerce')
    # ### end Alembic commands ###