"""empty message

Revision ID: 64038875a675
Revises: 7c8883c170bc
Create Date: 2023-12-02 13:16:11.767758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64038875a675'
down_revision = '7c8883c170bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('reviewId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reviewId'], ['reviews.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###
