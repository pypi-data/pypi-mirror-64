from unittest import TestCase
import command_history

class TestHistory(TestCase):
  def test_is_string(self):
    s = command_history.history()