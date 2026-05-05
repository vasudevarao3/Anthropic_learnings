def greetings():
    print("Hello World")


def calculate_pi():
    """
    Calculate pi to 5 decimal places (3.14159) using the Nilakantha series.
    The Nilakantha series converges faster than the Leibniz formula.
    
    Formula: pi = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - 4/(8*9*10) + ...
    
    Returns:
        float: Pi calculated to at least 5 decimal places
    """
    pi = 3.0
    sign = 1
    denominator = 2
    
    # Iterate until we have sufficient precision (5 decimal places)
    # We need more iterations to ensure accuracy to 5 decimal places
    for i in range(100000):
        term = 4.0 / (denominator * (denominator + 1) * (denominator + 2))
        pi += sign * term
        sign *= -1
        denominator += 2
        
    return round(pi, 5) 