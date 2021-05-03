"""added comment on spectra table

Revision ID: a5e549203f03
Revises: 0595e877f471
Create Date: 2021-04-29 14:46:12.394625

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a5e549203f03'
down_revision = '0595e877f471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'comments_on_spectra',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column(
            'ctype',
            sa.Enum('text', 'redshift', name='comment_types', create_type=False),
            nullable=True,
        ),
        sa.Column('attachment_name', sa.String(), nullable=True),
        sa.Column('attachment_bytes', sa.LargeBinary(), nullable=True),
        sa.Column('origin', sa.String(), nullable=True),
        sa.Column('spectrum_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('obj_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['obj_id'], ['objs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['spectrum_id'], ['spectra.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_comments_on_spectra_author_id'),
        'comments_on_spectra',
        ['author_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_comments_on_spectra_created_at'),
        'comments_on_spectra',
        ['created_at'],
        unique=False,
    )
    op.create_index(
        op.f('ix_comments_on_spectra_obj_id'),
        'comments_on_spectra',
        ['obj_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_comments_on_spectra_spectrum_id'),
        'comments_on_spectra',
        ['spectrum_id'],
        unique=False,
    )
    op.create_table(
        'group_comments_on_spectra',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('comments_on_spectr_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['comments_on_spectr_id'], ['comments_on_spectra.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'group_comments_on_spectra_forward_ind',
        'group_comments_on_spectra',
        ['group_id', 'comments_on_spectr_id'],
        unique=True,
    )
    op.create_index(
        'group_comments_on_spectra_reverse_ind',
        'group_comments_on_spectra',
        ['comments_on_spectr_id', 'group_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_group_comments_on_spectra_created_at'),
        'group_comments_on_spectra',
        ['created_at'],
        unique=False,
    )
    op.drop_index('ix_stream_photometry_created_at', table_name='stream_photometry')
    op.drop_index('stream_photometry_forward_ind', table_name='stream_photometry')
    op.drop_index('stream_photometry_reverse_ind', table_name='stream_photometry')
    op.drop_table('stream_photometry')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'stream_photometry',
        sa.Column(
            'created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            'modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('stream_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('photometr_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['photometr_id'],
            ['photometry.id'],
            name='stream_photometry_photometr_id_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['stream_id'],
            ['streams.id'],
            name='stream_photometry_stream_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='stream_photometry_pkey'),
    )
    op.create_index(
        'stream_photometry_reverse_ind',
        'stream_photometry',
        ['photometr_id', 'stream_id'],
        unique=False,
    )
    op.create_index(
        'stream_photometry_forward_ind',
        'stream_photometry',
        ['stream_id', 'photometr_id'],
        unique=True,
    )
    op.create_index(
        'ix_stream_photometry_created_at',
        'stream_photometry',
        ['created_at'],
        unique=False,
    )
    op.drop_index(
        op.f('ix_group_comments_on_spectra_created_at'),
        table_name='group_comments_on_spectra',
    )
    op.drop_index(
        'group_comments_on_spectra_reverse_ind', table_name='group_comments_on_spectra'
    )
    op.drop_index(
        'group_comments_on_spectra_forward_ind', table_name='group_comments_on_spectra'
    )
    op.drop_table('group_comments_on_spectra')
    op.drop_index(
        op.f('ix_comments_on_spectra_spectrum_id'), table_name='comments_on_spectra'
    )
    op.drop_index(
        op.f('ix_comments_on_spectra_obj_id'), table_name='comments_on_spectra'
    )
    op.drop_index(
        op.f('ix_comments_on_spectra_created_at'), table_name='comments_on_spectra'
    )
    op.drop_index(
        op.f('ix_comments_on_spectra_author_id'), table_name='comments_on_spectra'
    )
    op.drop_table('comments_on_spectra')
    # ### end Alembic commands ###
