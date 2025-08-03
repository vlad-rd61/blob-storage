import psycopg2

class CameraStorage:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cameras (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    active_file TEXT,
                    offset INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)
            self.conn.commit()

    def insert_camera(self, name, active_file=None, offset=0, is_active=True):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cameras (name, active_file, offset, is_active)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (name, active_file, offset, is_active))
            cam_id = cur.fetchone()[0]
            self.conn.commit()
            return cam_id

    def get_camera_by_name(self, name):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM cameras WHERE name = %s;", (name,))
            return cur.fetchone()

    def update_camera_offset(self, name, offset):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE cameras SET offset = %s WHERE name = %s;
            """, (offset, name))
            self.conn.commit()
