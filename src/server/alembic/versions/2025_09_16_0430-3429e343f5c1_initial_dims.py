"""Initial dims

Revision ID: 3429e343f5c1
Revises: 637f8aec5be5
Create Date: 2025-09-16 04:30:59.431710+00:00

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3429e343f5c1"
down_revision: str | Sequence[str] | None = "637f8aec5be5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    sa.Enum("repair_orders", "sku_receipts", name="tableenum", schema="dim").create(op.get_bind())

    op.create_table(
        "departments",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
            comment="Уникальный идентификатор записи",
        ),
        sa.Column("code", sa.String(), nullable=False, comment="Код в справочниках 1С"),
        sa.Column("name", sa.String(), nullable=False, comment="Наименование"),
        sa.Column("is_deleted", sa.Boolean(), server_default="false", nullable=False, comment="Пометка на удаление"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Создан"
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Обновлен",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_departments")),
        sa.UniqueConstraint("code", name=op.f("uq_departments_code")),
        schema="dim",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("departments", schema="dim")