import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

# Path to the database file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "patients.db"
DB_PATH = Path(os.environ.get("DATABASE_PATH", str(DEFAULT_DB_PATH)))


def get_connection() -> sqlite3.Connection:
    """Creates a connection to the SQLite database with row factory enabled."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes the database schema if tables do not already exist."""
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    mobile TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                );
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_patients_email ON patients(email);
                """
            )
    finally:
        conn.close()


def get_patient_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieves patient record by normalized lowercase email."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, full_name, dob, email, mobile, password_hash, created_at, status
            FROM patients
            WHERE lower(email) = lower(?)
            LIMIT 1;
            """,
            (email.strip(),),
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def get_patient_by_id(patient_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves patient record by unique ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, full_name, dob, email, mobile, created_at, status
            FROM patients
            WHERE id = ?
            LIMIT 1;
            """,
            (patient_id,),
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def create_patient(
    full_name: str,
    dob: str,
    email: str,
    mobile: str,
    password_hash: str,
    created_at: str,
) -> Dict[str, Any]:
    """Inserts a new patient record and returns the patient dictionary."""
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO patients (full_name, dob, email, mobile, password_hash, created_at, status)
                VALUES (?, ?, lower(?), ?, ?, ?, 'active');
                """,
                (
                    full_name.strip(),
                    dob.strip(),
                    email.strip(),
                    mobile.strip(),
                    password_hash,
                    created_at,
                ),
            )
            patient_id = cursor.lastrowid

        return {
            "id": patient_id,
            "full_name": full_name.strip(),
            "dob": dob.strip(),
            "email": email.strip().lower(),
            "mobile": mobile.strip(),
            "created_at": created_at,
            "status": "active",
        }
    finally:
        conn.close()


def update_patient_password(patient_id: int, new_password_hash: str) -> bool:
    """Updates the patient's password hash in the database."""
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE patients
                SET password_hash = ?
                WHERE id = ?;
                """,
                (new_password_hash, patient_id),
            )
            return cursor.rowcount > 0
    finally:
        conn.close()


def get_patient_by_mobile(mobile: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves patient record by matching mobile number, normalizing formatting.
    Safely matches exact formatted numbers or normalized trailing digit sequences.
    """
    cleaned = re.sub(r"[\s\-\(\)]", "", mobile.strip())
    digits_only = re.sub(r"\D", "", cleaned)
    if not digits_only or len(digits_only) < 10:
        return None

    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Direct lookup with cleaned string or with/without leading plus
        cursor.execute(
            """
            SELECT id, full_name, dob, email, mobile, password_hash, created_at, status
            FROM patients
            WHERE (mobile = ? OR mobile = ?) AND status = 'active'
            LIMIT 1;
            """,
            (
                cleaned,
                f"+{cleaned}" if not cleaned.startswith("+") else cleaned.lstrip("+"),
            ),
        )
        row = cursor.fetchone()
        if row:
            return dict(row)

        # Fallback: match by digit sequence (e.g. matching last 10 digits for local/intl formats)
        cursor.execute(
            """
            SELECT id, full_name, dob, email, mobile, password_hash, created_at, status
            FROM patients
            WHERE status = 'active';
            """
        )
        for r in cursor.fetchall():
            db_digits = re.sub(r"\D", "", r["mobile"])
            if db_digits == digits_only or (
                len(digits_only) >= 10
                and len(db_digits) >= 10
                and digits_only[-10:] == db_digits[-10:]
            ):
                return dict(r)

        return None
    finally:
        conn.close()
