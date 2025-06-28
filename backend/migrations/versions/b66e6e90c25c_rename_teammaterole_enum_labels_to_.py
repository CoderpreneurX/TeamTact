"""rename_teammaterole_enum_labels_to_uppercase

Revision ID: b66e6e90c25c
Revises: 72bfacfd767a
Create Date: 2025-06-19 03:53:57.478703

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b66e6e90c25c"
down_revision: Union[str, None] = "72bfacfd767a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Rename enum values from lowercase to UPPERCASE
    op.execute("ALTER TYPE teammaterole RENAME VALUE 'owner' TO 'OWNER'")
    op.execute("ALTER TYPE teammaterole RENAME VALUE 'admin' TO 'ADMIN'")
    op.execute("ALTER TYPE teammaterole RENAME VALUE 'viewer' TO 'VIEWER'")


def downgrade() -> None:
    """Downgrade schema."""

    # Rename enum values from UPPERCASE back to lowercase
    op.execute("ALTER TYPE teammaterole RENAME VALUE 'OWNER' TO 'owner'")
    op.execute("ALTER TYPE teammaterole RENAME VALUE 'ADMIN' TO 'admin'")
    op.execute("ALTER TYPE teammaterole RENAME VALUE 'VIEWER' TO 'viewer'")
