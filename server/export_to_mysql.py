"""
Kitchen Intelligence System — SQLite to MySQL Dump Generator
Exports all tables, schemas, and rows from the local SQLite database to a MySQL-compatible .sql file
that can be imported directly into phpMyAdmin or MySQL server.
"""

import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = BASE_DIR / "instance" / "kitchen_intelligence.db"
OUTPUT_SQL_PATH = BASE_DIR / "kitchen_intelligence_mysql.sql"

def export_sqlite_to_mysql():
    if not SQLITE_PATH.exists():
        print(f"[ERROR] SQLite database not found at {SQLITE_PATH}")
        return False

    print(f"Reading SQLite database: {SQLITE_PATH}")
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
    tables = [r[0] for r in cur.fetchall()]
    print(f"Found {len(tables)} tables to export.")

    sql_lines = [
        "-- =============================================================",
        "-- Kitchen Intelligence System - MySQL Database Export",
        "-- Compatible with phpMyAdmin / MySQL 5.7+ / MariaDB 10+",
        "-- =============================================================\n",
        "CREATE DATABASE IF NOT EXISTS `kitchen_intelligence` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "USE `kitchen_intelligence`;\n",
        "SET FOREIGN_KEY_CHECKS = 0;\n"
    ]

    total_rows = 0

    for table in tables:
        cur.execute(f'PRAGMA table_info("{table}");')
        cols_info = cur.fetchall()

        sql_lines.append(f"-- -------------------------------------------------------------")
        sql_lines.append(f"-- Table structure for `{table}`")
        sql_lines.append(f"-- -------------------------------------------------------------")
        sql_lines.append(f"DROP TABLE IF EXISTS `{table}`;")

        col_defs = []
        pk_cols = []

        for c in cols_info:
            cid, name, col_type, notnull, dflt_value, pk = c
            col_type = col_type.upper().strip()

            if "INT" in col_type:
                mysql_type = "INT"
            elif "VARCHAR" in col_type:
                mysql_type = col_type
            elif "TEXT" in col_type or "CLOB" in col_type:
                mysql_type = "TEXT"
            elif "FLOAT" in col_type or "REAL" in col_type or "DOUBLE" in col_type:
                mysql_type = "DOUBLE"
            elif "BOOLEAN" in col_type or "BOOL" in col_type:
                mysql_type = "TINYINT(1)"
            elif "DATE" in col_type:
                mysql_type = "DATE"
            elif "TIMESTAMP" in col_type or "DATETIME" in col_type:
                mysql_type = "DATETIME"
            else:
                mysql_type = "TEXT"

            col_def = f"  `{name}` {mysql_type}"
            if pk == 1:
                if "INT" in mysql_type:
                    col_def += " AUTO_INCREMENT"
                pk_cols.append(f"`{name}`")
            if notnull and pk == 0:
                col_def += " NOT NULL"
            if dflt_value is not None and not (pk == 1 and "INT" in mysql_type):
                col_def += f" DEFAULT {dflt_value}"

            col_defs.append(col_def)

        if pk_cols:
            col_defs.append(f"  PRIMARY KEY ({', '.join(pk_cols)})")

        create_stmt = f"CREATE TABLE `{table}` (\n" + ",\n".join(col_defs) + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n"
        sql_lines.append(create_stmt)

        cur.execute(f'SELECT * FROM "{table}";')
        rows = cur.fetchall()
        total_rows += len(rows)

        if rows:
            sql_lines.append(f"-- Dumping data for table `{table}` ({len(rows)} rows)")
            col_names = [f"`{c[1]}`" for c in cols_info]
            cols_str = f"({', '.join(col_names)})"

            chunk_size = 100
            for i in range(0, len(rows), chunk_size):
                chunk = rows[i:i + chunk_size]
                val_strs = []
                for row in chunk:
                    row_vals = []
                    for val in row:
                        if val is None:
                            row_vals.append("NULL")
                        elif isinstance(val, (int, float)):
                            row_vals.append(str(val))
                        elif isinstance(val, bool):
                            row_vals.append("1" if val else "0")
                        else:
                            escaped = str(val).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")
                            row_vals.append(f"'{escaped}'")
                    val_strs.append(f"  ({', '.join(row_vals)})")
                insert_stmt = f"INSERT INTO `{table}` {cols_str} VALUES\n" + ",\n".join(val_strs) + ";\n"
                sql_lines.append(insert_stmt)

        sql_lines.append("")

    sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;\n")

    with open(OUTPUT_SQL_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))

    file_size_mb = os.path.getsize(OUTPUT_SQL_PATH) / (1024 * 1024)
    print(f"[SUCCESS] Exported {len(tables)} tables ({total_rows} total rows) to {OUTPUT_SQL_PATH}")
    print(f"File size: {file_size_mb:.2f} MB")
    return True

if __name__ == "__main__":
    export_sqlite_to_mysql()
