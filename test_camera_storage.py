import unittest
import psycopg2
from camera_storage import CameraStorage

DSN = "dbname=testdb user=postgres password=postgres host=localhost port=5432"

class TestCameraStorage(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(DSN)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS cameras;")
        self.storage = CameraStorage(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_insert_and_fetch(self):
        cam_id = self.storage.insert_camera("cam01", "file01", 100, True)
        cam = self.storage.fetch_camera("cam01")
        self.assertIsNotNone(cam)
        self.assertEqual(cam[0], cam_id)
        self.assertEqual(cam[1], "cam01")
        self.assertEqual(cam[2], "file01")
        self.assertEqual(cam[3], 100)
        self.assertTrue(cam[4])

    def test_update_offset(self):
        self.storage.insert_camera("cam02", "file02", 0, True)
        self.storage.update_offset("cam02", 500)
        cam = self.storage.fetch_camera("cam02")
        self.assertEqual(cam[3], 500)

if __name__ == '__main__':
    unittest.main()
