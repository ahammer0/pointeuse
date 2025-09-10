import unittest

from lib.Periode.Periode import Periode


class TestPeriode(unittest.TestCase):
    # Sat Aug 09 2025 19:03:01 to Sun Aug 10 2025 19:03:01
    p1 = Periode((1, 1754758981, 1754845381))

    # splits into :
    # Sat Aug 09 2025 19:03:01 to Sat Aug 9 2025 23:59:59
    p2 = Periode((1, 1754758981, 1754776799))

    # Sun Aug 10 2025 00:00:00 to Sun Aug 10 2025 19:03:01
    p3 = Periode((1, 1754776800, 1754845381))

    def test_splitAtMidnight(self):
        pl = Periode.splitPeriodesAtMidnight([self.p1])
        self.assertEqual(repr(pl), repr([[self.p3], [self.p2]]))

    def test_splitAtMidnight_shouldSeparateDifferentDays(self):
        pl = Periode.splitPeriodesAtMidnight([self.p2, self.p3])
        self.assertEqual(repr(pl), repr([[self.p3], [self.p2]]))


if __name__ == "__main__":
    unittest.main()
