import asyncio
from datetime import datetime, timedelta, timezone

import asyncpg
import httpx

from app.tasks.celery_app import celery_app


@celery_app.task(name="send_appointment_reminders")
def send_appointment_reminders() -> dict:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(_send_reminders())
        return result
    finally:
        loop.close()


async def _send_reminders() -> dict:
    import os

    db_url = os.getenv("SUPABASE_DB_URL", "")
    fcm_key = os.getenv("FCM_SERVER_KEY", "")

    if not db_url:
        return {"status": "error", "message": "SUPABASE_DB_URL not configured"}

    dsn = db_url.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(dsn)

    try:
        now = datetime.now(timezone.utc)
        reminder_window = now + timedelta(hours=1)

        rows = await conn.fetch(
            """
            SELECT a.id, a.starts_at, a.patient_id, c.fcm_token, c.full_name as counselor_name,
                   p.full_name as patient_name
            FROM appointments a
            JOIN counselors c ON c.id = a.counselor_id
            JOIN patients p ON p.id = a.patient_id
            WHERE a.starts_at BETWEEN $1 AND $2
              AND a.reminder_sent = false
              AND a.status = 'scheduled'
              AND c.fcm_token IS NOT NULL
            """,
            now,
            reminder_window,
        )

        sent_count = 0
        for row in rows:
            success = await _send_fcm_notification(
                fcm_key=fcm_key,
                token=row["fcm_token"],
                title="Upcoming Session",
                body=f"Session with {row['patient_name']} starts at {row['starts_at'].strftime('%I:%M %p')}",
            )
            if success:
                await conn.execute(
                    "UPDATE appointments SET reminder_sent = true WHERE id = $1",
                    row["id"],
                )
                sent_count += 1

        return {"status": "ok", "reminders_sent": sent_count}
    finally:
        await conn.close()


async def _send_fcm_notification(
    fcm_key: str,
    token: str,
    title: str,
    body: str,
) -> bool:
    if not fcm_key or not token:
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://fcm.googleapis.com/fcm/send",
            headers={
                "Authorization": f"key={fcm_key}",
                "Content-Type": "application/json",
            },
            json={
                "to": token,
                "notification": {
                    "title": title,
                    "body": body,
                },
            },
            timeout=10.0,
        )
        return response.status_code == 200
