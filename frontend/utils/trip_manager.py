import uuid
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not found. Check your .env file."
    )

def create_trip(user_id, destination):

    trip_id = (
        f"{destination.lower().replace(' ', '_')}_"
        f"{uuid.uuid4().hex[:8]}"
    )

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO trips
                (
                    trip_id,
                    user_id,
                    destination
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    trip_id,
                    user_id,
                    destination
                )
            )

        conn.commit()

    return trip_id


def get_trips(user_id):

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    trip_id,
                    destination
                FROM trips
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,)
            )

            rows = cur.fetchall()

    return rows