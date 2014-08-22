"""empty message

Revision ID: 39c05d4e41c
Revises: None
Create Date: 2014-08-17 21:41:30.763420

"""

# revision identifiers, used by Alembic.
revision = '39c05d4e41c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('join_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###