def minimumFlips(target: str) -> int:
    """
    Calculates the minimum number of flips required to transform a binary string to the target state.

    Args:
        target: The target binary string (e.g., "0011").

    Returns:
        The minimum number of flips required (int), or None if the input is not a valid string.
    """
    
    if not isinstance(target, str) or not all(char in "01" for char in target):
        return None  # Check for valid input
    
    flips = 0
    current_state = '0'

    for char in target:
        if char != current_state:
            flips += 1
            current_state = char

    return flips

# Test cases for minimumFlips
assert minimumFlips("0011") == 1
assert minimumFlips("101") == 2
assert minimumFlips("0") == 0
assert minimumFlips("111000") == 2
assert minimumFlips("11011101111") == 3
assert minimumFlips(None) == None
assert minimumFlips("abc") == None

if __name__ == '__main__':
    target = input().strip()
    result = minimumFlips(target)
    print(result)
