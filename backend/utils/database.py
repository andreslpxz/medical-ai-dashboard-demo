import aiosqlite
import json
import os

DB_PATH = "backend/reports.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                metadata TEXT,
                report_json TEXT,
                latency_ms INTEGER,
                model_version TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def save_report(status, metadata, report_json, latency_ms, model_version):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO reports (status, metadata, report_json, latency_ms, model_version)
            VALUES (?, ?, ?, ?, ?)
        """, (status, json.dumps(metadata), json.dumps(report_json), latency_ms, model_version))
        await db.commit()
        return cursor.lastrowid

async def get_report(report_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM reports WHERE id = ?", (report_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                res = dict(row)
                res['metadata'] = json.loads(res['metadata']) if res['metadata'] else None
                res['report_json'] = json.loads(res['report_json']) if res['report_json'] else None
                return res
            return None
