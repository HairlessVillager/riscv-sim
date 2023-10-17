from .config import SIZE


class Instruction:

    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def run_by(self, simulator):
        raise NotImplementedError

    def __index__(self):
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.name} {int(self):0=#10x} {vars(self)}>"


class InstructionR(Instruction):

    def __init__(self, *, rd, rs1, rs2):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def __index__(self):
        res = ((self.funct7 << 25)
              | (self.rs2 << 20)
              | (self.rs1 << 15)
              | (self.funct3 << 12)
              | (self.rd << 7)
              | (self.opcode << 0)
        )
        return res


class InstructionI(Instruction):

    def __init__(self, *, rd, imm, rs1):
        self.rd = rd
        self.imm = imm
        self.rs1 = rs1

    def __index__(self):
        return (((self.imm & 0b111111111111) << 20)
               | (self.rs1 << 15)
               | (self.funct3 << 12)
               | (self.rd << 7)
               | (self.opcode << 0)
        )


class InstructionS(Instruction):

    def __init__(self, *, rs1, rs2, imm):
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm

    def __index__(self):
        return (((self.imm & 0b111111100000) >> 5 << 25)
              | (self.rs2 << 20)
              | (self.rs1 << 15)
              | (self.funct3 << 12)
              | ((self.imm & 0b000000011111) >> 0 << 7)
              | (self.opcode << 0)
        )


class InstructionSB(Instruction):

    def __init__(self, *, rs1, rs2, imm):
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm

    def __index__(self):
        return (((self.imm & 0b100000000000) >> 11 << 31)
              | ((self.imm & 0b001111110000) >> 4 << 25)
              | (self.rs2 << 20)
              | (self.rs1 << 15)
              | (self.funct3 << 12)
              | ((self.imm & 0b000000001111) >> 0 << 8)
              | ((self.imm & 0b010000000000) >> 10 << 7)
              | (self.opcode << 0)
        )


class InstructionU(Instruction):

    def __init__(self, *, rd, imm):
        self.rd = rd
        self.imm = imm

    def __index__(self):
        return ((self.imm << 12)
              | (self.rd << 7)
              | (self.opcode << 0)
        )


class InstructionUJ(Instruction):

    def __init__(self, *, rd, imm):
        self.rd = rd
        self.imm = imm

    def __index__(self):
        return (((self.imm & 0b10000000000000000000) >> 19 << 31)
              | ((self.imm & 0b00000000001111111111) >> 0 << 21)
              | ((self.imm & 0b00000000010000000000) >> 10 << 20)
              | ((self.imm & 0b01111111100000000000) >> 11 << 12)
              | (self.rd << 7)
              | (self.opcode << 0)
        )


class AddInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b000
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 + v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class SubInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b000
    funct7 = 0b0100000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 - v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class SllInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b001
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 << v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class SrlInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b101
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 >> v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class SraInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b101
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=True)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=True)
        simulator.registers[self.rd].set(SIZE, v_rs1 >> v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class XorInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b100
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 ^ v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class OrInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b110
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 | v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class AndInstruction(InstructionR):
    opcode = 0b0110011
    funct3 = 0b111
    funct7 = 0b0000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v_rs1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v_rs2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        simulator.registers[self.rd].set(SIZE, v_rs1 & v_rs2)
        pc = simulator.pc
        simulator.pc = pc + 4


class LbInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 0b000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 1, signed=True)
        simulator.registers[self.rd].set(1, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class LhInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 0b001

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 2, signed=True)
        simulator.registers[self.rd].set(2, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class LwInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 0b010

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 4, signed=True)
        simulator.registers[self.rd].set(4, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class LdInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 0b011

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 8, signed=True)
        simulator.registers[self.rd].set(8, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class LbuInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 1, signed=False)
        simulator.registers[self.rd].set(1, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class LhuInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 0b101

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 2, signed=False)
        simulator.registers[self.rd].set(2, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class LwuInstruction(InstructionI):
    opcode = 0b0000011
    funct3 = 0b110

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        base_addr = simulator.registers[self.rs1].get(SIZE, signed=False)
        v = simulator.memory.read(base_addr+self.imm, 4, signed=False)
        simulator.registers[self.rd].set(4, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class AddiInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 0b000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) + self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class SlliInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 0b001
    funct6 = 0b000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) << self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class SrliInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 0b101
    funct6 = 0b000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) >> self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class SraiInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 0b101
    funct6 = 0b010000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=True) >> self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class XoriInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) ^ self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class OriInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 0b110

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) | self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class AndiInstruction(InstructionI):
    opcode = 0b0010011
    funct3 = 0b111

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) & self.imm
        simulator.registers[self.rd].set(SIZE, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class JalrInstruction(InstructionI):
    opcode = 0b1100111
    funct3 = 0b000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs1].get(SIZE, signed=False) + self.imm
        pc = simulator.pc
        simulator.registers[self.rd].set(SIZE, pc + 4)
        simulator.pc = v


class SbInstruction(InstructionS):
    opcode = 0b0100011
    funct3 = 0b000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs2].get(1, signed=False)
        addr = simulator.registers[self.rs1].get(SIZE, signed=False) + self.imm
        simulator.memory.write(addr, 1, v)
        simulator.registers[self.rd].set(SIZE, pc + 4)
        simulator.pc = v


class ShInstruction(InstructionS):
    opcode = 0b0100011
    funct3 = 0b001

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs2].get(2, signed=False)
        addr = simulator.registers[self.rs1].get(SIZE, signed=False) + self.imm
        simulator.memory.write(addr, 2, v)
        simulator.registers[self.rd].set(SIZE, pc + 4)
        simulator.pc = v


class SwInstruction(InstructionS):
    opcode = 0b0100011
    funct3 = 0b010

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs2].get(4, signed=False)
        addr = simulator.registers[self.rs1].get(SIZE, signed=False) + self.imm
        simulator.memory.write(addr, 4, v)
        simulator.registers[self.rd].set(SIZE, pc + 4)
        simulator.pc = v


class SdInstruction(InstructionS):
    opcode = 0b0100011
    funct3 = 0b111

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = simulator.registers[self.rs2].get(8, signed=False)
        addr = simulator.registers[self.rs1].get(SIZE, signed=False) + self.imm
        simulator.memory.write(addr, 8, v)
        simulator.registers[self.rd].set(SIZE, pc + 4)
        simulator.pc = v


class BeqInstruction(InstructionSB):
    opcode = 0b1100011
    funct3 = 0b000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v1 = simulator.registers[self.rs1].get(SIZE, signed=True)
        v2 = simulator.registers[self.rs2].get(SIZE, signed=True)
        pc = simulator.pc
        if v1 == v2:
            pc += self.imm * 2
        else:
            pc += 4
        simulator.pc = pc


class BneInstruction(InstructionSB):
    opcode = 0b1100011
    funct3 = 0b001

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v1 = simulator.registers[self.rs1].get(SIZE, signed=True)
        v2 = simulator.registers[self.rs2].get(SIZE, signed=True)
        pc = simulator.pc
        if v1 != v2:
            pc += self.imm * 2
        else:
            pc += 4
        simulator.pc = pc


class BltInstruction(InstructionSB):
    opcode = 0b1100011
    funct3 = 0b100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v1 = simulator.registers[self.rs1].get(SIZE, signed=True)
        v2 = simulator.registers[self.rs2].get(SIZE, signed=True)
        pc = simulator.pc
        if v1 < v2:
            pc += self.imm * 2
        else:
            pc += 4
        simulator.pc = pc


class BgeInstruction(InstructionSB):
    opcode = 0b1100011
    funct3 = 0b101

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v1 = simulator.registers[self.rs1].get(SIZE, signed=True)
        v2 = simulator.registers[self.rs2].get(SIZE, signed=True)
        pc = simulator.pc
        if v1 >= v2:
            pc += self.imm * 2
        else:
            pc += 4
        simulator.pc = pc


class BltuInstruction(InstructionSB):
    opcode = 0b1100011
    funct3 = 0x110

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        pc = simulator.pc
        if v1 < v2:
            pc += self.imm * 2
        else:
            pc += 4
        simulator.pc = pc


class BgeuInstruction(InstructionSB):
    opcode = 0b1100011
    funct3 = 0b111

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v1 = simulator.registers[self.rs1].get(SIZE, signed=False)
        v2 = simulator.registers[self.rs2].get(SIZE, signed=False)
        pc = simulator.pc
        if v1 >= v2:
            pc += self.imm * 2
        else:
            pc += 4
        simulator.pc = pc


class LuiInstruction(InstructionU):
    opcode = 0b0110111

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        v = self.imm << 12
        simulator.registers[self.rd].set(4, v)
        pc = simulator.pc
        simulator.pc = pc + 4


class JalInstruction(InstructionUJ):
    opcode = 0b1101111

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = __class__.__name__

    def run_by(self, simulator):
        pc = simulator.pc
        v = pc + self.imm * 2
        simulator.registers[self.rd].set(SIZE, pc + 4)
        simulator.pc = v

