import os
import unittest
import py_presi.build


class TestMe(unittest.TestCase):
    def test_me(self):
        py_presi.build.build()
        INDEX_PATH = os.path.dirname(py_presi.build.README_PATH)
        self.assertTrue(os.path.exists(os.path.join(INDEX_PATH, "index.html")))
