import unittest
import math
from main import calculate_pi


class TestPiCalculation(unittest.TestCase):
    """Test cases for the calculate_pi function"""
    
    def test_pi_value(self):
        """Test that calculated pi matches expected value to 5 decimal places"""
        calculated_pi = calculate_pi()
        expected_pi = 3.14159
        self.assertEqual(calculated_pi, expected_pi,
                        f"Expected {expected_pi}, but got {calculated_pi}")
    
    def test_pi_accuracy(self):
        """Test that calculated pi is close to math.pi to 5 decimal places"""
        calculated_pi = calculate_pi()
        actual_pi = round(math.pi, 5)
        self.assertEqual(calculated_pi, actual_pi,
                        f"Calculated pi {calculated_pi} doesn't match math.pi rounded to 5 places: {actual_pi}")
    
    def test_pi_type(self):
        """Test that the function returns a float"""
        calculated_pi = calculate_pi()
        self.assertIsInstance(calculated_pi, float,
                            f"Expected float, but got {type(calculated_pi)}")
    
    def test_pi_range(self):
        """Test that pi is within a reasonable range"""
        calculated_pi = calculate_pi()
        self.assertGreater(calculated_pi, 3.14,
                          f"Pi value {calculated_pi} is too small")
        self.assertLess(calculated_pi, 3.15,
                       f"Pi value {calculated_pi} is too large")
    
    def test_pi_precision(self):
        """Test that pi has exactly 5 decimal places"""
        calculated_pi = calculate_pi()
        # Convert to string and check decimal places
        pi_str = str(calculated_pi)
        if '.' in pi_str:
            decimal_places = len(pi_str.split('.')[1])
            self.assertLessEqual(decimal_places, 5,
                                f"Pi has more than 5 decimal places: {pi_str}")


if __name__ == '__main__':
    # Run the tests
    print("Testing calculate_pi() function...\n")
    unittest.main(verbosity=2)
