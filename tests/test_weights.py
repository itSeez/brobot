import io
import unittest
from contextlib import redirect_stdout

from brobot import weights


class WeightsTests(unittest.TestCase):
    def render_solution(self, first, second):
        output = io.StringIO()
        with redirect_stdout(output):
            weights.print_solution((0, first, second))
        return output.getvalue()

    def test_equal_targets_minimize_common_plates(self):
        output = io.StringIO()
        with redirect_stdout(output):
            weights.main(185, 185)
        self.assertEqual(
            output.getvalue(),
            '\nCommon plates: 45 25\nFirst Set:    \nSecond Set:   \n',
        )

    def test_second_pass_minimizes_each_set(self):
        for group in ('First Set:', 'Second Set:'):
            with self.subTest(group=group):
                first = (5, 10, 25, 35)
                second = (5, 45)
                if group == 'Second Set:':
                    first, second = second, first
                output = self.render_solution(first, second)
                lines = dict(line.split(':', 1) for line in output.strip().splitlines())
                self.assertEqual(lines['Common plates'].strip(), '5')
                self.assertEqual(lines[group[:-1]].strip(), '45 25')

    def test_bar_only_has_no_plates(self):
        output = io.StringIO()
        with redirect_stdout(output):
            weights.main(45, 45)
        self.assertEqual(
            output.getvalue(),
            '\nCommon plates:\nFirst Set:    \nSecond Set:   \n',
        )

    def test_preserves_fractional_and_already_minimal_plates(self):
        self.assertEqual(
            self.render_solution((35, 5, 45, 10), (35, 5, 25, 2.5)),
            '\nCommon plates: 35 5\nFirst Set:     45 10\nSecond Set:    25 2.5\n',
        )

    def test_common_plates_respect_multiplicity(self):
        self.assertEqual(
            self.render_solution((10, 10, 2.5), (10, 2.5)),
            '\nCommon plates: 10 2.5\nFirst Set:     10\nSecond Set:   \n',
        )


if __name__ == '__main__':
    unittest.main()
