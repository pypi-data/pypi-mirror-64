import os
import unittest

import qtpy.QtWebEngineWidgets  # noqa: F401
from qtpy.QtWidgets import QApplication

from vidify import Platform, CURRENT_PLATFORM


if QApplication.instance() is None:
    _ = QApplication(["vidify"])
TRAVIS = "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true"
SKIP_MSG = "Skipping this test as it won't work on the current system."


class SwSpotifyTest(unittest.TestCase):
    @unittest.skipIf(TRAVIS or CURRENT_PLATFORM not in (Platform.MACOS,
                     Platform.WINDOWS), SKIP_MSG)
    def test_simple(self):
        from vidify.api.spotify.swspotify import SwSpotifyAPI
        api = SwSpotifyAPI()
        api.connect_api()
        api._refresh_metadata()
        api.event_loop()


if __name__ == '__main__':
    unittest.main()
