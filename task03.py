# Task 3: Pytest
# - Write a function is_adult(age) that returns True for ages 18 and above.
# - Raise a ValueError for negative ages.
# - Write 3 test cases for ages 17, 18, and -1.
# - Ensure all tests pass.
import pytest

def is_adult(age):
    if age < 0:
        raise ValueError("Age? can't be negative dude :)")
    elif age >= 18:
        return True
    else:
        return False

def test_is_adult():                    # asserstion simply gonna tell us if something is true or false
    assert is_adult(18) == True         # here we are testing the function is_adult with different ages and checking if the output is as expected
    assert is_adult(17) == False  
    with pytest.raises(ValueError):     # here we are testing if the function raises a ValueError for negative ages
        is_adult(-1)