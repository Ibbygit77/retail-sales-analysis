"""Run every query in a .sql file against sales.db and print the results.

Usage:  python run_query.py sql/01_explore.sql
Queries are separated by semicolons. Lines starting with -- are comments.
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def print_table(cursor, rows):
    headers = [d[0] for d in cursor.description]
    cells = [[("" if v is None else str(v)) for v in row] for row in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) if cells else len(h)
              for i, h in enumerate(headers)]
    line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * len(line))
    for r in cells:
        print(" | ".join(v.ljust(w) for v, w in zip(r, widths)))
    print(f"({len(rows)} rows)\n")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python run_query.py path/to/file.sql")
    sql = Path(sys.argv[1]).read_text(encoding="utf-8")
    conn = sqlite3.connect(ROOT / "sales.db")
    for statement in sql.split(";"):
        code = "\n".join(l for l in statement.splitlines()
                         if not l.strip().startswith("--")).strip()
        if not code:
            continue
        print(">>> " + code.splitlines()[0] + (" ..." if "\n" in code else ""))
        try:
            cur = conn.execute(code)
            if cur.description is None:      # e.g. CREATE VIEW: no rows to show
                print("OK\n")
            else:
                print_table(cur, cur.fetchmany(50))
        except sqlite3.Error as e:
            print(f"ERROR: {e}\n")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
