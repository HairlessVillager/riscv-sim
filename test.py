""" Unit Test for all

Note
====
Initial test cases are based on Wuhan University course
熊小兵 - 计算机组成原理 (2023-2024-1)-3140520011017
homework
"""

import unittest

from riscvsim import (
    InstructionFactory,
    Registers,
    Register,
    Simulator,
    Memory,
)
from riscvsim.config import *


class TestInstructionFactory(unittest.TestCase):

    def test_get(self):
        cases = [
            ["add x3, x2, x1",      0x001101b3],
            ["addi x2, x1, -100",   0xf9c08113],
            ["lw x2, -100(x1)",     0xf9c0a103],
            ["slli x2, x1, 12",     0x00c09113],
            ["jalr x2, -100(x1)",   0xf9c08167],
            ["sw x2, 100(x1)",      0x0620a223],
            ["beq x1, x2, -100",    0xf2208ce7],
            ["lui x1, 1234",        0x004d20b7],
            ["jal x1, -200",        0xe71ff0ef],
            # TODO: more and more
        ]
        for i, v in cases:
            i = InstructionFactory.get(i)
            self.assertEqual(int(i), v, f"{i=}\n{int(i):0=#32b}\n{v:0=#32b}")
        for i, v in cases:
            i = InstructionFactory.get(i)
            self.assertEqual(int(i), v, f"{i=}\n{int(i):0=#32b}\n{v:0=#32b}")

        # TODO: exceptions should be tested

    @unittest.skip("to implement")
    def test_get_text(self):
        text = r"""
            add x0, x0, x0      ; Instruction0
        label2:
            add x0, x0, x0      ; Instruction1
            add x0, x0, x0      ; Instruction2
            beq x1, x2, label1  ; Instruction3
            add x0, x0, x0      ; Instruction4
            jal x1, label2      ; Instruction5
        label1:
            add x0, x0, x0      ; Instruction6
            add x0, x0, x0      ; Instruction7
        """
        self.assertEqual(
            hex(InstructionFactory.get_text(text)[5]),
            "0xff1ff0ef"
        )
        self.assertEqual(
            hex(InstructionFactory.get_text(text)[3]),
            "0x00208667"
        )


class TestRegister(unittest.TestCase):

    def test_set_get(self):
        cases = []

        for bytes_num in [1, 2, 4, 8]:
            f = lambda x, y, z: cases.append([bytes_num, x, y, z])
            bits = bytes_num * 8
            f(-(1<<(bits-1)), False, 1<<(bits-1))
            f(-(1<<(bits-1)), True, -(1<<(bits-1)))
            f(-1, False, (1<<bits)-1)
            f(-1, True, -1)
            f(0, False, 0)
            f(0, True, 0)
            f(1, False, 1)
            f(1, True, 1)
            f((1<<(bits-1))-1, False, (1<<(bits-1))-1)
            f((1<<(bits-1))-1, True, (1<<(bits-1))-1)
            f(1<<(bits-1), False, 1<<(bits-1))
            f(1<<(bits-1), True, -(1<<(bits-1)))
            f((1<<bits)-1, False, (1<<bits)-1)
            f((1<<bits)-1, True, -1)

        for bytes_num, write, signed, expected in cases:
            r = Register(bytes_num=bytes_num)
            r.set(bytes_num, write)
            read = r.get(bytes_num, signed=signed)
            self.assertEqual(read, expected,
                f"{r=} {bytes_num, write, signed, expected}")

    def test_set_get_with_exception(self):
        cases = []

        for bytes_num in [1, 2, 4, 8]:
            f = lambda x, y, z: cases.append([bytes_num, x, y, z])
            bits = bytes_num * 8
            f(-(1<<(bits-1))-1, False, ValueError)
            f((1<<bits), False, ValueError)

        for bytes_num, write, signed, expection in cases:
            with self.assertRaises(expection):
                r = Register(bytes_num=bytes_num)
                r.set(bytes_num, write)
                read = r.get(bytes_num, signed=signed)


class TestRegisters(unittest.TestCase):

    def test_init(self):
        registers = Registers(
            0x00, 0x11, 0x22, 0x33, 0x44,
            t5=0x55, s6=0x66)
        self.assertEqual(registers[0].get(SIZE, signed=False), 0x00)
        self.assertEqual(registers[1].get(SIZE, signed=False), 0x11)
        self.assertEqual(registers[2].get(SIZE, signed=False), 0x22)
        self.assertEqual(registers[3].get(SIZE, signed=False), 0x33)
        self.assertEqual(registers[4].get(SIZE, signed=False), 0x44)
        self.assertEqual(registers["t5"].get(SIZE, signed=False), 0x55)
        self.assertEqual(registers["s6"].get(SIZE, signed=False), 0x66)
        # TODO: exceptions should be tested

    def test_setter_getter(self):
        from riscvsim.simulator import REGISTERS_DIR
        registers_dir = REGISTERS_DIR

        registers = Registers()
        for r, i in registers_dir.items():
            magic_1 = 0x00114514
            magic_2 = 0x01919810
            registers[i].set(SIZE, magic_1)
            self.assertEqual(registers[r].get(SIZE, signed=False), magic_1,
                             f"{r=}, {i=}, {registers[r]=}")
            registers[r].set(SIZE, magic_2)
            self.assertEqual(registers[i].get(SIZE, signed=False), magic_2,
                             f"{r=}, {i=}, {registers[i]=}")
        # TODO: exceptions should be tested


class TestMemory(unittest.TestCase):

    def test_read_write(self):
        memory = Memory(addr_max=0xffffffff)

        memory.write(0x00000000, 1,               0x01)
        memory.write(0x00000001, 1,               0x23)
        memory.write(0x00000002, 2,             0x6745)
        memory.write(0x00000004, 4,         0xefcdab89)
        memory.write(0x00000008, 8, 0x1032547698badcfe)
        memory_values = [
            # 0x00000000
            0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
            # 0x00000008
            0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10,
        ]
        for i, x in enumerate(memory_values):
            self.assertEqual(memory.read(i, 1, signed=False), x, f"\n{str(memory)}\n{i=}")

        self.assertEqual(memory.read(0x00000000, 4, signed=True), 1732584193)
        self.assertEqual(memory.read(0x00000000, 4, signed=False), 1732584193)
        self.assertEqual(memory.read(0x00000004, 4, signed=True), -271733879)
        self.assertEqual(memory.read(0x00000004, 4, signed=False), 4023233417)

        self.assertEqual(memory.read(0x00000002, 2, signed=False), 0x6745)
        self.assertEqual(memory.read(0x00000001, 1, signed=False), 0x23)
        self.assertEqual(memory.read(0x00000000, 1, signed=False), 0x01)

        with self.assertRaisesRegex(TypeError,
                r"missing 1 required keyword-only argument: 'signed'"):
            memory.read(0x00000000, 1)
        with self.assertRaisesRegex(TypeError,
                r"takes \d+ positional arguments but \d+ were given"):
            memory.read(0x00000000, 1, True)


class TestSimulator(unittest.TestCase):

    def test_setter_getter(self):
        sim = Simulator(x2=-4321, x3=1234)
        sim.x1 = 0x10
        sim.pc = 0x20
        sim[0x00001111] = 0x30

        self.assertEqual(sim.registers["x1"].get(SIZE, signed=False), 0x10)
        self.assertEqual(sim.registers["x2"].get(SIZE, signed=False), 0xffffffffffffef1f)
        self.assertEqual(sim.registers["x3"].get(SIZE, signed=False), 1234)
        self.assertEqual(sim.pc, 0x20)
        self.assertEqual(sim.memory[0x00001111].get(SIZE, signed=False), 0x30)

    def test_copy(self):
        sim = Simulator(x1=0x11, x2=0x22, pc=0xff)
        for addr in range(128):
            sim[addr] = addr

        sim_copy = sim.copy()
        self.assertIsNot(sim, sim_copy)
        self.assertIsNot(sim.registers, sim_copy.registers)
        self.assertIsNot(sim.memory, sim_copy.memory)

        for r in range(32):
            self.assertIsNot(sim.registers[r], sim_copy.registers[r])
            self.assertEqual(
                sim.registers[r].get(SIZE, signed=False),
                sim_copy.registers[r].get(SIZE, signed=False),
            )
        for addr in range(128):
            self.assertIsNot(sim.memory[addr], sim_copy.memory[addr])
            self.assertEqual(
                sim.memory[addr].get(1, signed=False),
                sim_copy.memory[addr].get(1, signed=False),
            )

    def test_step(self):
        # TODO: more and more
        sim = Simulator(x1=1234, x2=-4321, x3=1000, pc=8000)

        start = 1230
        vs = [-10, 20, -30, 40]
        for i, v in enumerate(vs):
            sim.memory[start + i].set(1, v % 256)
        factory = InstructionFactory()
        cases = [
            ["addi x1, x0, -100",   "x1",   -100      ],
            ["lw x2, -4(x1)",       "x2",   0x28e214f6],
            ["lwu x2, -4(x1)",      "x2",   0x28e214f6],
            ["lui x1, 1234",        "x1",   5054464   ],
            ["andi x2, x1, 100",    "x2",   64        ],
            ["sra x3, x2, x1",      "x3",   -1        ],
            ["blt x2, x1, -100",    "pc",   7800      ],
            ["bltu x2, x1, 100",    "pc",   8004      ],
            ["jal x1, -200",        "x1",   8004      ],
            ["jal x1, -200",        "pc",   7600      ],
            ["jalr x2, -100(x1)",   "x2",   8004      ],
            ["jalr x2, -100(x1)",   "pc",   1134      ],
    # TODO: ["auipc x1, 100",       "x1",   417600    ],
    # TODO: ["slti x2, x1, -123",   "x2",   0         ],
    # TODO: ["sltiu x2, x1, -123",  "x2",   1         ],
            ["beq x2, x1, 100",     "pc",   8004      ],
        ]
        for i, r, v in cases:
            sim_copy = sim.copy()
            i = factory.get(i)
            sim_copy.step(i)
            if r == "pc":
                read = sim_copy.pc
            else:
                read = sim_copy.registers[r].get(SIZE, signed=True)
            self.assertEqual(read, v, f"{i=} {r=} {read=:#x} {v=:#x}")
        # TODO: exceptions should be tested

    @unittest.skip("to implement")
    def test_load(self):
        pass

    @unittest.skip("to implement")
    def test_run(self):
        pc_orig = 0x8000
        x2_orig = 0x114514
        x2_change = 0x10123
        sim = Simulator(pc=pc_orig, x2=x2_orig)

        text = r"""
            lui x1, 16
            add x2, x2, x1
            addi x2, x2, 0x123
        """
        sim_copy = sim.copy()
        text = InstructionFactory.get_text(text)
        sim_copy.load(0x00000000, text)
        sim_copy.run(steps=3)
        self.assertEqual(sim_copy.x2, x2_orig + x2_change)

        text = r"""
            lui x1, 16
            addi x1, x1, 0x123
            add x2, x2, x1
        """
        text = InstructionFactory.get_text(text)
        sim_copy = sim.copy()
        sim_copy.load(0x00000000, text)
        sim_copy.run(steps=3)
        self.assertEqual(sim_copy.x2, x2_orig + x2_change)

        text = r"""
            addi x1, x0, 16
            slli x1, x1, 12
            addi x1, x1, 0x123
            add x2, x2, x1
        """
        sim_copy = sim.copy()
        sim_copy.load(0x00000000, text)
        sim_copy.run(steps=3)
        self.assertEqual(sim_copy.x2, x2_orig + x2_change)


if __name__ == "__main__":
    unittest.main(failfast=True)

