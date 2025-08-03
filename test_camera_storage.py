import unittest
import psycopg2
from datetime import date, timedelta
from camera_storage import CameraStorage

DSN = "dbname=testdb user=postgres password=secret host=127.0.0.1"

class TestCameraStorage(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(DSN)
        self.storage = CameraStorage(self.conn)
        self.storage.create_table()
        self.storage.clear_table()

    def tearDown(self):
        self.storage.clear_table()
        self.conn.close()

    def test_insert_and_fetch(self):
        self.storage.insert_camera("cam_001", "Test Camera")
        state = self.storage.get_camera_state("cam_001")
        self.assertIsNotNone(state)
        self.assertEqual(state[0], date.today())
        self.assertEqual(state[1], 0)

    def test_offset_update(self):
        self.storage.insert_camera("cam_001")
        self.storage.update_offset("cam_001", 512)
        state = self.storage.get_camera_state("cam_001")
        self.assertEqual(state[1], 512)

    def test_rotate_file(self):
        self.storage.insert_camera("cam_001")
        with self.conn.cursor() as cur:
            cur.execute("UPDATE cameras SET active_file = %s WHERE camera_uid = %s;",
                        (date.today() - timedelta(days=1), "cam_001"))
        self.storage.rotate_file_if_needed("cam_001")
        state = self.storage.get_camera_state("cam_001")
        self.assertEqual(state[0], date.today())
        self.assertEqual(state[1], 0)

if __name__ == '__main__':
    unittest.main()
