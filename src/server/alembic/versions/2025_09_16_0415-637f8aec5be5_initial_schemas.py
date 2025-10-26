"""Initial schemas

Revision ID: 637f8aec5be5
Revises:
Create Date: 2025-09-16 04:15:16.860905+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "637f8aec5be5"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA dim")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA dim")
