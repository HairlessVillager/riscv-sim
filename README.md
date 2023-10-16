# riscv-sim
An friendly and easy-to-use RISC-V simulator in Python.

## Quickstart

See [example.py](./example.py)

```python
>>> from riscvsim import *
>>> sim = Simulator(pc=0x8000, x5=0x114000, x6=0x000514)
>>> sim[0x00001003] = 0x19
>>> sim[0x00001002] = 0x26
>>> sim[0x00001001] = 0x08
>>> sim[0x00001000] = 0x17
>>> print(sim)
Simulator Info
===========================================
pc=32768 0x8000
Registers:
 x0                    0 0x0000000000000000
 x1                    0 0x0000000000000000
 x2                    0 0x0000000000000000
 x3                    0 0x0000000000000000
 x4                    0 0x0000000000000000
 x5              1130496 0x0000000000114000
 x6                 1300 0x0000000000000514
 x7                    0 0x0000000000000000
...
x31                    0 0x0000000000000000
Memory:
0x00001000  17 08 26 19   .. .. .. ..
>>> inst = InstructionFactory.get("add x7, x5, x6")
>>> inst
<Instruction 0x006283b3 {'rd': 7, 'rs1': 5, 'rs2': 6}>
>>> sim.step(inst)
>>> hex(sim.x5)
0x114000
>>> hex(sim.x6)
0x514
>>> hex(sim.x7)
0x114514
>>> sim.x5 = 0x00001000
>>> sim.step(InstructionFactory.get("lw x7, 0(x5)"))
>>> hex(sim.x7)
0x19260817
>>> print(sim)
Simulator Info
===========================================
pc=32776 0x8008
Registers:
 x0                    0 0x0000000000000000
 x1                    0 0x0000000000000000
 x2                    0 0x0000000000000000
 x3                    0 0x0000000000000000
 x4                    0 0x0000000000000000
 x5                 4096 0x0000000000001000
 x6                 1300 0x0000000000000514
 x7            421922839 0x0000000019260817
 x8                    0 0x0000000000000000
...
x31                    0 0x0000000000000000
Memory:
0x00001000  17 08 26 19   .. .. .. ..
```

## Document

See docstring in source code. No independent document pages here so far.

## Test

Run `python -m unittest test`.

## Contributing

If you want to contribute to this repo...
- New an issue or pull request for bug you find or feature/enhancement you want.
- Complete the `TODO`s in source code. Note that you are always required to add tests.
- Add/Check/Fix each docstring you are interested in. You might need to see [some examples in numpy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html).
- Add/Check/Fix [tests](./test.py) for feature you are interested in. You might need to see [the docs of unittest](https://docs.python.org/zh-cn/3/library/unittest.html).

