"""Data-quality checks for generated or ingested client-impact tables."""

from __future__ import annotations

from typing import Any

from .generate import TABLE_NAMES


def quality_report(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Return deterministic quality metrics without mutating the input tables."""
    errors: list[str] = []
    warnings: list[str] = []
    table_counts = {name: len(tables.get(name, [])) for name in TABLE_NAMES}

    missing_tables = sorted(set(TABLE_NAMES) - set(tables))
    errors.extend(f"missing table: {name}" for name in missing_tables)

    client_rows = tables.get("clients", [])
    client_ids = [row.get("client_id") for row in client_rows]
    if len(client_ids) != len(set(client_ids)):
        errors.append("clients.client_id contains duplicates")
    known_clients = {client_id for client_id in client_ids if client_id is not None}

    for table_name, rows in tables.items():
        for row_number, row in enumerate(rows, start=1):
            client_id = row.get("client_id")
            if client_id is not None and client_id not in known_clients:
                errors.append(f"{table_name} row {row_number} has unknown client_id")
            for field, value in row.items():
                if value is None and field not in {"women_loan_control_score", "women_income_control_score"}:
                    warnings.append(f"{table_name}.{field} row {row_number} is missing")

    for row_number, row in enumerate(tables.get("households", []), start=1):
        if row.get("household_size", 0) < 1:
            errors.append(f"households row {row_number} has invalid household_size")
        if row.get("monthly_household_income", 0) <= 0:
            errors.append(f"households row {row_number} has invalid monthly_household_income")

    for row_number, row in enumerate(tables.get("loans", []), start=1):
        for field in ("loan_amount", "monthly_debt_payment"):
            if row.get(field, 0) <= 0:
                errors.append(f"loans row {row_number} has invalid {field}")

    for row_number, row in enumerate(tables.get("agency_surveys", []), start=1):
        for field in ("women_loan_control_score", "women_income_control_score"):
            value = row.get(field)
            if value is not None and not 0 <= value <= 1:
                errors.append(f"agency_surveys row {row_number} has invalid {field}")

    if not client_rows:
        warnings.append("clients table is empty")
    return {
        "ok": not errors,
        "table_counts": table_counts,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }