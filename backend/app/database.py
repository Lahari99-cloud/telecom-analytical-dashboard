import csv
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / 'database'
DB_PATH = DB_DIR / 'telecom_catalog.db'
DATA_PATH = BASE_DIR / 'data' / 'telecom_sample_data.csv'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    segment TEXT NOT NULL,
    product TEXT NOT NULL,
    revenue REAL NOT NULL,
    churn REAL NOT NULL,
    arpu REAL NOT NULL,
    nps REAL NOT NULL,
    latency REAL NOT NULL,
    risk REAL NOT NULL,
    month TEXT NOT NULL
);
'''

def get_conn() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force: bool = False) -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(SCHEMA)
    count = cur.execute('SELECT COUNT(*) AS c FROM customers').fetchone()['c']
    if force or count == 0:
        cur.execute('DELETE FROM customers')
        with DATA_PATH.open(newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            cur.execute('''
                INSERT INTO customers(region, segment, product, revenue, churn, arpu, nps, latency, risk, month)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (r['region'], r['segment'], r['product'], float(r['revenue']), float(r['churn']), float(r['arpu']), float(r['nps']), float(r['latency']), float(r['risk']), r['month']))
        conn.commit()
        count = len(rows)
    conn.close()
    return {'database': str(DB_PATH), 'rows': count, 'status': 'ready'}

def query_rows(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    conn = get_conn()
    try:
        rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()
    return rows

def replace_from_csv(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    required = {'region','segment','product','revenue','churn','arpu','nps','latency','risk','month'}
    if not rows:
        raise ValueError('CSV is empty')
    missing = required - set(rows[0].keys())
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(SCHEMA)
    cur.execute('DELETE FROM customers')
    for r in rows:
        cur.execute('''
            INSERT INTO customers(region, segment, product, revenue, churn, arpu, nps, latency, risk, month)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (r['region'], r['segment'], r['product'], float(r['revenue']), float(r['churn']), float(r['arpu']), float(r['nps']), float(r['latency']), float(r['risk']), r['month']))
    conn.commit()
    conn.close()
    return {'status': 'loaded', 'rows': len(rows)}
