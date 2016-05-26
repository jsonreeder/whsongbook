import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from splinter import Browser

# Configure your app to use the testing database
# os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from whsongbook import app

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)

    def test_visit_index(self):
        self.browser.visit("http://0.0.0.0:8080/")
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
       
    def test_visit_browse(self):
        self.browser.visit("http://0.0.0.0:8080/browse")
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/browse")

    def test_visit_about(self):
        self.browser.visit("http://0.0.0.0:8080/about")
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/about")

    def test_visit_redirect(self):
        """
        When a non-existent song url is requested, the browser should be
        redirected to the browse page
        """
        self.browser.visit("http://0.0.0.0:8080/songs/lugubrious_lima_beans-love_lichtenstein")
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/browse")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
