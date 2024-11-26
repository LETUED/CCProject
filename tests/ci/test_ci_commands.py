import unittest
from unittest.mock import patch
from click.testing import CliRunner
from ci_cd_tool.commands.ci import ci_group

class TestCICommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        
    def test_ci_build_command(self):
        result = self.runner.invoke(ci_group, ['build'])
        self.assertEqual(result.exit_code, 0)
        
    def test_ci_test_command(self):
        result = self.runner.invoke(ci_group, ['test'])
        self.assertEqual(result.exit_code, 0)