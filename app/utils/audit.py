from app.core.database import SessionLocal
from app.models.audit_log import AuditLog


def log_action(action: str, target: str = None, details: str = None, user: str = "system"):
    """Write an entry to the audit log."""
    db = SessionLocal()
    try:
        entry = AuditLog(
            action=action,
            user=user,
            target=target,
            details=details,
        )
        db.add(entry)
        db.commit()
        return entry.id
    except Exception as e:
        print(f"⚠️ Audit log failed: {e}")
    finally:
        db.close()