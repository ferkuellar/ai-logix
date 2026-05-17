"""add user driver relationship

Revision ID: 20260517_0002
Revises: 20260517_0001
Create Date: 2026-05-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260517_0002"
down_revision: Union[str, None] = "20260517_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("driver_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index(op.f("ix_users_driver_id"), "users", ["driver_id"], unique=False)
    op.create_foreign_key(
        "fk_users_driver_id_drivers",
        "users",
        "drivers",
        ["driver_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_users_driver_id_drivers", "users", type_="foreignkey")
    op.drop_index(op.f("ix_users_driver_id"), table_name="users")
    op.drop_column("users", "driver_id")
