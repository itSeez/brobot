import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from brobot import console


class ConsoleTests(unittest.TestCase):
    def test_weights_dispatches_integer_targets(self):
        with patch('sys.argv', ['brobot', 'weights', '185', '185']):
            with patch('brobot.weights.main') as main:
                console.run()
        main.assert_called_once_with(185, 185)

    def test_weights_help_describes_subcommand_arguments(self):
        output = io.StringIO()
        with patch('sys.argv', ['brobot', 'weights', '--help']):
            with redirect_stdout(output), self.assertRaises(SystemExit) as exit:
                console.run()
        self.assertEqual(exit.exception.code, 0)
        self.assertIn('brobot weights [-h] t1 t2', output.getvalue())
        self.assertIn('First weight target.', output.getvalue())

    def test_invalid_arguments_report_parser_errors(self):
        for args in ([], ['unknown'], ['weights'], ['weights', '185'],
                     ['weights', '185', '185', '185'], ['weights', 'abc', '185']):
            with self.subTest(args=args):
                output = io.StringIO()
                with patch('sys.argv', ['brobot', *args]), redirect_stderr(output):
                    with self.assertRaises(SystemExit) as exit:
                        console.run()
                self.assertEqual(exit.exception.code, 2)
                self.assertIn('error:', output.getvalue())


if __name__ == '__main__':
    unittest.main()
