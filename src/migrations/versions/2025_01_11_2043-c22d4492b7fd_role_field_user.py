"""role field user

Revision ID: c22d4492b7fd
Revises: 841d4635cd26
Create Date: 2025-01-11 20:43:58.359112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c22d4492b7fd"
down_revision: Union[str, None] = "841d4635cd26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("role", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "role")
    # ### end Alembic commands ###
