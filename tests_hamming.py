"""
def test_hammingDecode():
    # Decoding when no errors leads to sequence recovering
    assert hamming748_decode([1, 1, 0, 1, 0, 0, 1, 0]) == [1, 1, 0, 1] 
    assert hamming748_decode([1, 1, 0, 0, 1, 1, 0, 0]) == [1, 1, 0, 0]
    assert hamming748_decode([1, 1, 1, 1, 1, 1, 1, 1]) == [1, 1, 1, 1]
    assert hamming748_decode([0, 1, 1, 1, 1, 0, 0, 0]) == [0, 1, 1, 1]
    assert hamming748_decode([0, 1, 1, 0, 0, 1, 1, 0]) == [0, 1, 1, 0]
    assert hamming748_decode([0, 0, 1, 1, 0, 0, 1, 1]) == [0, 0, 1, 1]
    assert hamming748_decode([0, 0, 1, 0, 1, 1, 0, 1]) == [0, 0, 1, 0]
    assert hamming748_decode([0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]) == [0, 0, 1, 1, 0, 0, 1, 0]
    # Ensure that one error is detected, and corrected
    assert hamming748_decode([1, 1, 0, 1, 0, 0, 0, 0]) == [1, 1, 0, 1]
    assert hamming748_decode([1, 1, 0, 0, 1, 1, 0, 0]) == [1, 1, 0, 0]
    assert hamming748_decode([1, 0, 1, 1, 1, 1, 1, 1]) == [1, 1, 1, 1]
    assert hamming748_decode([0, 1, 1, 1, 1, 0, 0, 0]) == [0, 1, 1, 1]
    assert hamming748_decode([0, 1, 1, 0, 0, 1, 1, 0]) == [0, 1, 1, 0]
    assert hamming748_decode([0, 0, 1, 1, 0, 0, 1, 0]) == [0, 0, 1, 1]
    assert hamming748_decode([0, 0, 1, 0, 1, 1, 0, 1]) == [0, 0, 1, 0]    
    # Ensure that two errors cannot be corrected
    assert hamming748_decode([1, 0, 1, 1, 0, 0, 1, 0]) != [1, 1, 0, 1]
    assert hamming748_decode([1, 1, 1, 1, 1, 1, 0, 0]) != [1, 1, 0, 0]
    assert hamming748_decode([0, 1, 1, 0, 1, 1, 1, 1]) != [1, 1, 1, 1]
    assert hamming748_decode([1, 0, 1, 1, 1, 0, 0, 0]) != [0, 1, 1, 1]
    assert hamming748_decode([1, 1, 1, 1, 0, 1, 1, 0]) != [0, 1, 1, 0]
    assert hamming748_decode([0, 1, 0, 1, 0, 0, 1, 1]) != [0, 0, 1, 1]
    assert hamming748_decode([0, 1, 0, 0, 1, 1, 0, 1]) != [0, 0, 1, 0]
"""
