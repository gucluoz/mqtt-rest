"""empty message

Revision ID: 7c9fdf98c4cd
Revises: None
Create Date: 2016-01-19 11:04:49.729795

"""

# revision identifiers, used by Alembic.
revision = '7c9fdf98c4cd'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temprature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('m1', sa.String(length=100), nullable=True),
    sa.Column('m2', sa.String(length=100), nullable=True),
    sa.Column('m3', sa.String(length=100), nullable=True),
    sa.Column('m4', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('asset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=300), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('building_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('buildingItem_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['buildingItem_id'], ['building_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor')
    op.drop_table('building_item')
    op.drop_table('asset')
    op.drop_table('user')
    op.drop_table('temprature')
    ### end Alembic commands ###
