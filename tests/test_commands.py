import unittest
from unittest.mock import patch

from jarvis import CommandExecutor


class CommandExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.executor = CommandExecutor()

    @patch("jarvis.webbrowser.open")
    def test_browser_command(self, open_mock):
        result = self.executor.execute("tarayıcı aç")
        self.assertTrue(result.handled)
        open_mock.assert_called_once()

    def test_unknown_command(self):
        result = self.executor.execute("bilinmeyen komut")
        self.assertFalse(result.handled)

    def test_exit_command(self):
        result = self.executor.execute("çıkış")
        self.assertTrue(result.should_exit)


if __name__ == "__main__":
    unittest.main()
