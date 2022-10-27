"""urls

Revision ID: 8938d92d2981
Revises: b80f0f4115bb
Create Date: 2022-10-27 15:22:43.628550

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '8938d92d2981'
down_revision = 'b80f0f4115bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('key', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('key', name=op.f('pk_urls'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('url_key', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['url_key'], ['urls.key'], name=op.f('fk_users_url_key_urls')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('urls')
    # ### end Alembic commands ###
