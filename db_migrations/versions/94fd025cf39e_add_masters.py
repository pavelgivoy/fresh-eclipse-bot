"""add masters

Revision ID: 94fd025cf39e
Revises: 98d831bd39e2
Create Date: 

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94fd025cf39e'
down_revision = '98d831bd39e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('masters',
                    sa.Column('link', sa.Text(), nullable=False),
                    sa.Column('guild', sa.String(length=3), nullable=True),
                    sa.Column('castle', sa.Text(), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('bs_guru', sa.Text(), nullable=True),
                    sa.Column('bs_level', sa.Integer(), nullable=True),
                    sa.Column('alch_guru', sa.Text(), nullable=True),
                    sa.Column('alch_level', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['guild'], ['guilds.tag'], ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('link'),
                    sa.UniqueConstraint('username')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('masters')
    # ### end Alembic commands ###
