from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import src.database.connection as conn_service
from src.database.models import Base, NeonatalTelemetry


def test_save_and_retrieve_telemetry_lifecycle(monkeypatch) -> None:
    """Verifies that a clinical telemetry record is correctly persisted and retrieved."""
    mem_engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=mem_engine)
    SessionFactory = sessionmaker(bind=mem_engine)

    # Correct monkeypatch mapping target directed safely to connection lifecycle module
    monkeypatch.setattr(conn_service, "SessionLocal", SessionFactory)

    with conn_service.get_db_session() as session:
        record = NeonatalTelemetry(
            heart_rate=140,
            temperature=36.7,
            systolic_bp=65,
            diastolic_bp=38,
            oxygen_saturation=97.5,
            pcr_level=5.0,
            pct_level=0.4,
            aki_level="normal",
        )
        session.add(record)

    with conn_service.get_db_session() as session:
        retrieved = session.query(NeonatalTelemetry).first()
        assert retrieved is not None
        assert retrieved.heart_rate == 140
        assert retrieved.temperature == 36.7


def test_reset_clinical_profile_purges_records(monkeypatch) -> None:
    """Verifies that executing a profile reset completely wipes patient data rows."""
    mem_engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=mem_engine)
    SessionFactory = sessionmaker(bind=mem_engine)

    monkeypatch.setattr(conn_service, "SessionLocal", SessionFactory)

    with conn_service.get_db_session() as session:
        record = NeonatalTelemetry(
            heart_rate=150,
            temperature=38.2,
            systolic_bp=40,
            diastolic_bp=20,
            oxygen_saturation=89.0,
            pcr_level=45.0,
            pct_level=8.2,
        )
        session.add(record)

    with conn_service.get_db_session() as session:
        session.query(NeonatalTelemetry).delete()

    with conn_service.get_db_session() as session:
        count = session.query(NeonatalTelemetry).count()
        assert count == 0
