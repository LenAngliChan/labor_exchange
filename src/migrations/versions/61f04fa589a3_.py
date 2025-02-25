"""empty message

Revision ID: 61f04fa589a3
Revises: 
Create Date: 2024-01-16 23:56:31.273222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61f04fa589a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False, comment='ID пользователя'),
    sa.Column('email', sa.String(), nullable=False, comment='Эл.Адресс пользователя'),
    sa.Column('name', sa.String(), nullable=False, comment='Имя пользователя'),
    sa.Column('hashed_password', sa.String(), nullable=False, comment='Пароль пользователя'),
    sa.Column('is_company', sa.Boolean(), nullable=False, comment='Флаг компании'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Дата создания'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Jobs',
    sa.Column('id', sa.Integer(), nullable=False, comment='ID вакансии'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='ID создателя'),
    sa.Column('title', sa.String(), nullable=False, comment='Заголовок'),
    sa.Column('description', sa.String(), nullable=True, comment='Описание'),
    sa.Column('salary_from', sa.NUMERIC(), nullable=False, comment='Оплата от..'),
    sa.Column('salary_to', sa.NUMERIC(), nullable=False, comment='Оплата до..'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='Активная'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Дата создания'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Responses',
    sa.Column('id', sa.Integer(), nullable=False, comment='ID отклика'),
    sa.Column('job_id', sa.Integer(), nullable=True, comment='ID вакансии'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='ID соискателя'),
    sa.Column('message', sa.String(), nullable=True, comment='Сообщение'),
    sa.ForeignKeyConstraint(['job_id'], ['Jobs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Responses')
    op.drop_table('Jobs')
    op.drop_table('Users')
    # ### end Alembic commands ###
