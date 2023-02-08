def slump(test_slump: float, min_slump: float, max_slump: float) -> int:
    """ Checks if the slump value is within the specified range.
        -1 if test_slump < min_slump; 1 if test_slump > max_slump; else 0
    """
    if test_slump < min_slump:
        return 1
    if test_slump > max_slump:
        return 2
    return 0

def air(test_air: float, min_air: float, max_air: float) -> int:
    """ Checks if the air value is within the specified range.
        -1 if test_air < min_air; 1 if test_air > max_air; else 0
    """
    if test_air < min_air:
        return 1
    if test_air > max_air:
        return 2
    return 0