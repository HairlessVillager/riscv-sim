SIZE = 8    # unit: 1 byte

REGISTERS_DIR = {
                # USE                               SAVER
    "zero": 0,  # The constant value 0              N.A.
    "x0":   0,
    "ra":   1,  # Return address                    Caller
    "x1":   1,
    "sp":   2,  # Stack pointer                     Callee
    "x2":   2,
    "gp":   3,  # Global pointer                    -
    "x3":   3,
    "tp":   4,  # Thread pointer                    -
    "x4":   4,
    "t0":   5,  # Temporaries                       Caller
    "x5":   5,
    "t1":   6,  #
    "x6":   6,
    "t2":   7,  #
    "x7":   7,
    "s0":   8,  # Saved register/Frame pointer      Callee
    "sp":   8,
    "x8":   8,
    "s1":   9,  # Saved register                    Callee
    "x9":   9,
    "a0":   10, # Function arguments/Return values  Caller
    "x10":  10,
    "a1":   11, #
    "x11":  11,
    "a2":   12, # Function arguments                Caller
    "x12":  12,
    "a3":   13, #
    "x13":  13,
    "a4":   14, #
    "x14":  14,
    "a5":   15, #
    "x15":  15,
    "a6":   16, #
    "x16":  16,
    "a7":   17, #
    "x17":  17,
    "s2":   18, # Saved registers                   Callee
    "x18":  18,
    "s3":   19, #
    "x19":  19,
    "s4":   20, #
    "x20":  20,
    "s5":   21, #
    "x21":  21,
    "s6":   22, #
    "x22":  22,
    "s7":   23, #
    "x23":  23,
    "s8":   24, #
    "x24":  24,
    "s9":   25, #
    "x25":  25,
    "s10":  26, #
    "x26":  26,
    "s11":  27, #
    "x27":  27,
    "t3":   28, # Temporaries                       Caller
    "x28":  28,
    "t4":   29, #
    "x29":  29,
    "t5":   30, #
    "x30":  30,
    "t6":   31, #
    "x31":  31,
}
