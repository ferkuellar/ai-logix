from pathlib import Path

from app.db.base import Base
from app.models.audit_log import AuditLog
from app.models.delivery_event import DeliveryEvent
from app.models.driver import Driver
from app.models.order_state import OrderState
from app.models.store import Store
from app.models.user import User


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_alembic_files_exist():
    assert (BACKEND_ROOT / "alembic.ini").is_file()
    assert (BACKEND_ROOT / "alembic" / "env.py").is_file()
    assert (BACKEND_ROOT / "alembic" / "script.py.mako").is_file()


def test_baseline_migration_exists_with_upgrade_and_downgrade():
    versions = BACKEND_ROOT / "alembic" / "versions"
    migrations = list(versions.glob("*_baseline_schema.py"))

    assert migrations
    content = migrations[0].read_text(encoding="utf-8")
    assert "def upgrade()" in content
    assert "def downgrade()" in content


def test_user_driver_relationship_migration_exists_with_upgrade_and_downgrade():
    versions = BACKEND_ROOT / "alembic" / "versions"
    migrations = list(versions.glob("*_add_user_driver_relationship.py"))

    assert migrations
    content = migrations[0].read_text(encoding="utf-8")
    assert "def upgrade()" in content
    assert "def downgrade()" in content
    assert "driver_id" in content


def test_metadata_contains_expected_tables():
    expected_tables = {
        "users",
        "drivers",
        "stores",
        "delivery_events",
        "order_states",
        "audit_logs",
    }

    assert expected_tables.issubset(set(Base.metadata.tables))


def test_user_metadata_contains_driver_id():
    assert "driver_id" in Base.metadata.tables["users"].columns
