import unittest
import psycopg2
from camera_storage import CameraStorage

DSN = "dbname=testdb user=postgres password=postgres host=localhost port=5432"

class TestCameraStorage(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(DSN)
        self.conn.autocommit = True
        self.storage = CameraStorage(self.conn)

        # Ensure clean test table
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS cameras;")
        self.storage.create_table()

    def tearDown(self):
        self.conn.close()

    def test_insert_and_fetch(self):
        camera_id = self.storage.insert_camera("cam-001", "file001", 100)
        camera = self.storage.get_camera_by_name("cam-001")
        self.assertIsNotNone(camera)
        self.assertEqual(camera[0], camera_id)
        self.assertEqual(camera[1], "cam-001")
        self.assertEqual(camera[2], "file001")
        self.assertEqual(camera[3], 100)
        self.assertEqual(camera[4], True)

    def test_update_offset(self):
        self.storage.insert_camera("cam-002", "file002", 0)
        self.storage.update_camera_offset("cam-002", 200)
        updated = self.storage.get_camera_by_name("cam-002")
        self.assertEqual(updated[3], 200)

if __name__ == "__main__":
    unittest.main()
