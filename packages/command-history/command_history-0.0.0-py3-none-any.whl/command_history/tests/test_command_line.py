from unittest import TestCase
from command_history.history import main

class TestCmd(TestCase):
  def test_basic(self):
    main()