import psycopg2
from datetime import date, timedelta

class CameraStorage:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)
        self.conn.autocommit = True

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS cameras (
                id SERIAL PRIMARY KEY,
                camera_uid TEXT UNIQUE NOT NULL,
                description TEXT,
                active BOOLEAN DEFAULT TRUE,
                retention_days INTEGER DEFAULT 30,
                active_file DATE,
                active_offset BIGINT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

    def insert_camera(self, camera_uid, description='', retention_days=30):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cameras (camera_uid, description, retention_days, active_file)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (camera_uid) DO NOTHING;
            """, (camera_uid, description, retention_days, date.today()))

    def update_offset(self, camera_uid, bytes_written):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE cameras
                SET active_offset = active_offset + %s
                WHERE camera_uid = %s;
            """, (bytes_written, camera_uid))

    def rotate_file_if_needed(self, camera_uid):
        today = date.today()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT active_file FROM cameras WHERE camera_uid = %s;
            """, (camera_uid,))
            result = cur.fetchone()
            if result and result[0] != today:
                cur.execute("""
                    UPDATE cameras
                    SET active_file = %s, active_offset = 0
                    WHERE camera_uid = %s;
                """, (today, camera_uid))

    def get_camera_state(self, camera_uid):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT active_file, active_offset FROM cameras WHERE camera_uid = %s;
            """, (camera_uid,))
            return cur.fetchone()
