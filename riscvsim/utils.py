def signed_as(x, /, *, bits, strict=True):
    if not isinstance(x, int):
        raise TypeError(f"The 'x' should be 'int', "
                        f"got {type(x)}.")
    if x < 0:
        raise ValueError(f"The 'x' should be >= 0, "
                         f"got {x}.")
    if strict and x >= (1 << bits):
        raise ValueError(f"In strict mode, the 'x' "
                         f"should be < {1 << bits=}, "
                         f"got {x}.")
    y = x & ((1 << bits) - 1)

    # If the highest bit is 1
    if x & (1 << (bits - 1)):
        y -= (1 << bits)

    return y

