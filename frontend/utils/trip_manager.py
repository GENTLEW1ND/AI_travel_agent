# import uuid
# import os
# import psycopg
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError(
#         "DATABASE_URL not found. Check your .env file."
#     )

# def init_db():

#     with psycopg.connect(DATABASE_URL) as conn:

#         with conn.cursor() as cur:

#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS trips (
#                     trip_id VARCHAR(255) PRIMARY KEY,
#                     user_id VARCHAR(255) NOT NULL,
#                     destination VARCHAR(255) NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """)

#         conn.commit()


# def create_trip(user_id, destination):

#     trip_id = (
#         f"{destination.lower().replace(' ', '_')}_"
#         f"{uuid.uuid4().hex[:8]}"
#     )

#     with psycopg.connect(DATABASE_URL) as conn:

#         with conn.cursor() as cur:

#             cur.execute(
#                 """
#                 INSERT INTO trips
#                 (
#                     trip_id,
#                     user_id,
#                     destination
#                 )
#                 VALUES
#                 (
#                     %s,
#                     %s,
#                     %s
#                 )
#                 """,
#                 (
#                     trip_id,
#                     user_id,
#                     destination
#                 )
#             )

#         conn.commit()

#     return trip_id


# def get_trips(user_id):
#     print(f"Loading trips for user: {user_id}")
#     with psycopg.connect(DATABASE_URL) as conn:

#         with conn.cursor() as cur:

#             cur.execute(
#                 """
#                 SELECT
#                     trip_id,
#                     destination
#                 FROM trips
#                 WHERE user_id = %s
#                 ORDER BY created_at DESC
#                 """,
#                 (user_id,)
#             )

#             rows = cur.fetchall()

#     return rows


import uuid
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env file.")


def init_db():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(255) PRIMARY KEY,
                    display_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS trips (
                    trip_id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL REFERENCES users(user_id),
                    destination VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        conn.commit()


def get_or_create_user(user_id: str, display_name: str = "Traveler", email: str = None) -> str:
    """
    If user_id exists, return it.
    If not, create it with the given display_name and email.
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT user_id FROM users WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()

            if row:
                print(f"DEBUG [db] existing user: {email} ({user_id})")
                return user_id

            cur.execute(
                "INSERT INTO users (user_id, display_name, email) VALUES (%s, %s, %s)",
                (user_id, display_name, email)
            )
            print(f"DEBUG [db] created user: {email} ({user_id})")

        conn.commit()

    return user_id


def create_trip(user_id, destination):
    trip_id = (
        f"{destination.lower().replace(' ', '_')}_"
        f"{uuid.uuid4().hex[:8]}"
    )

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO trips (trip_id, user_id, destination)
                VALUES (%s, %s, %s)
                """,
                (trip_id, user_id, destination)
            )
        conn.commit()

    return trip_id


def get_trips(user_id):
    print(f"DEBUG [db] loading trips for user: {user_id}")
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT trip_id, destination
                FROM trips
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            rows = cur.fetchall()

    return rows