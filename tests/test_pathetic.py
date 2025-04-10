import unittest
from pathetic import FileTool, DirTool, RunInDir
import os

class TestPathetic(unittest.TestCase):

    def setUp(self):
        self.test_file = "testfile.txt"
        self.test_dir = "testdir"

    def tearDown(self):
        if os.path.isfile(self.test_file):
            os.remove(self.test_file)
        if os.path.isdir(self.test_dir):
            os.rmdir(self.test_dir)

    def test_create_and_remove_file(self):
        ft = FileTool(self.test_file)
        self.assertFalse(os.path.isfile(self.test_file))
        ft.create()
        self.assertTrue(os.path.isfile(self.test_file))
        ft.remove()
        self.assertFalse(os.path.exists(self.test_file))

    def test_create_and_remove_dir(self):
        dt = DirTool(self.test_dir)
        self.assertFalse(os.path.isdir(self.test_dir))
        dt.create()
        self.assertTrue(os.path.isdir(self.test_dir))
        dt.remove()
        self.assertFalse(os.path.exists(self.test_dir))

    def test_run_in_dir_changes_working_directory(self):
        dt = DirTool(self.test_dir)
        dt.create_if_missing()
        original_dir = os.getcwd()
        working_dir = os.path.abspath(self.test_dir)
        with RunInDir(self.test_dir):
            self.assertEqual(os.getcwd(), working_dir)
        self.assertEqual(os.getcwd(), original_dir)

        # Clean up
        dt.remove_if_present()

if __name__ == '__main__':
    unittest.main()
