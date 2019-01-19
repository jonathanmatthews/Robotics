import unittest
import current_dir
from Code.times import times


class Tests(unittest.TestCase):
    def test(self):
        self.assertEqual(times(3, 4), 12)

    def test2(self):
        self.assertEqual(times(1, 2), 2)


if __name__ == '__main__':
    unittest.main()
