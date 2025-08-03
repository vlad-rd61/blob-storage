import psycopg2

class CameraStorage:
    def __init__(self, conn):
        self.conn = conn
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cameras (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    active_file TEXT,
                    "offset" INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)
            self.conn.commit()

    def insert_camera(self, name, active_file=None, offset=0, is_active=True):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cameras (name, active_file, "offset", is_active)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (name, active_file, offset, is_active))
            camera_id = cur.fetchone()[0]
            self.conn.commit()
            return camera_id

    def update_offset(self, name, offset):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE cameras SET "offset" = %s WHERE name = %s;
            """, (offset, name))
            self.conn.commit()

    def fetch_camera(self, name):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, active_file, "offset", is_active
                FROM cameras
                WHERE name = %s;
            """, (name,))
            return cur.fetchone()
