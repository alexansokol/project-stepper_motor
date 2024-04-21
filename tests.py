import unittest
from unittest.mock import patch
from gui import calculate_time, calculate_acceleration, calculate_position

class TestStepperMotorSimulator(unittest.TestCase):
    def test_calculate_time(self):
        self.assertAlmostEqual(calculate_time(1000, 100, 0), 10.0)
        self.assertAlmostEqual(calculate_time(1000, 100, 50), 20.0)

    def test_calculate_acceleration(self):
        self.assertAlmostEqual(calculate_acceleration(1000, 100, 0), 10.0)
        self.assertAlmostEqual(calculate_acceleration(1000, 100, 50), 5.0)

    def test_calculate_position(self):
        self.assertAlmostEqual(calculate_position(5, 0, 10), 125.0)
        self.assertAlmostEqual(calculate_position(10, 50, 5), 550.0)

if __name__ == '__main__':
    unittest.main()
