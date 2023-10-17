from . import instructions


instruction_classes = {
    "add":  instructions.AddInstruction,
    "sub":  instructions.SubInstruction,
    "sll":  instructions.SllInstruction,
    "xor":  instructions.XorInstruction,
    "srl":  instructions.SrlInstruction,
    "sra":  instructions.SraInstruction,
    "or":   instructions.OrInstruction,
    "and":  instructions.AndInstruction,
    "lb":   instructions.LbInstruction,
    "lh":   instructions.LhInstruction,
    "lw":   instructions.LwInstruction,
    "ld":   instructions.LdInstruction,
    "lbu":  instructions.LbuInstruction,
    "lhu":  instructions.LhuInstruction,
    "lwu":  instructions.LwuInstruction,
    "addi": instructions.AddiInstruction,
    "slli": instructions.SlliInstruction,
    "xori": instructions.XoriInstruction,
    "srli": instructions.SrliInstruction,
    "srai": instructions.SraiInstruction,
    "ori":  instructions.OriInstruction,
    "andi": instructions.AndiInstruction,
    "jalr": instructions.JalrInstruction,
    "sb":   instructions.SbInstruction,
    "sh":   instructions.ShInstruction,
    "sw":   instructions.SwInstruction,
    "sd":   instructions.SdInstruction,
    "beq":  instructions.BeqInstruction,
    "bne":  instructions.BneInstruction,
    "blt":  instructions.BltInstruction,
    "bge":  instructions.BgeInstruction,
    "bltu": instructions.BltuInstruction,
    "bgeu": instructions.BgeuInstruction,
    "lui":  instructions.LuiInstruction,
    "jal":  instructions.JalInstruction,
}


class InstructionFactory:

    @classmethod
    def get(cls, x):
        if isinstance(x, str):
            tokens = cls.__extract_tokens(x)
            instruction = cls.__translate(tokens)
        elif isinstance(x, int):
            instruction = cls.__translate_int(x)
        return instruction

    @classmethod
    def get_text(cls, text):
        # TODO: ugly, refactor this
        labels = {}
        text = text.splitlines()

        def remove_comment(line):
            semicolon_idx = line.find(";")
            if semicolon_idx == -1:
                semicolon_idx = None
            return line[:semicolon_idx]
        text = list(map(remove_comment, text))
        text = [_.strip() for _ in text]

        # get labels and offsets
        index = 0
        for line in text:
            if line.endswith(":"):
                label = line.rstrip(":")
                labels[label] = index
            else:
                index += 1
        text = list(filter(lambda x: x.rstrip(":") not in labels, text))

        def replace_labels_with_offsets(curr_line):
            curr, line = curr_line
            for label, index in labels.items():
                offset = (index - curr) * 2
                line = line.replace(label, str(offset))
            return line
        text = list(map(replace_labels_with_offsets, enumerate(text)))
        text = list(filter(lambda x: x and not x.isspace(), text))

        text = [cls.get(_) for _ in text]
        return text

    @classmethod
    def __extract_tokens(cls, x):
        tokens = x.lower() \
            .replace(",", " ") \
            .replace("(", " ") \
            .replace(")", " ") \
            .split()
        return tokens

    @classmethod
    def __translate_int(cls, value):
        opcode = (value >> 0) & 0b1111111
        funct3 = (value >> 12) & 0b111
        funct7 = (value >> 25) & 0b1111111
        rd = (value >> 7) & 0b11111
        rs1 = (value >> 15) & 0b11111
        rs2 = (value >> 20) & 0b11111

        instructions_ = instruction_classes.copy().values()
        instructions_ = list(filter(
            lambda i: i.opcode == opcode,
            instructions_
        ))

        # Ugly. Is there any way to use issubclass() in match-case?
        match instructions_[0].mro()[1]:
            case instructions.InstructionR:
                instructions_ = list(filter(
                    lambda i: i.funct3 == funct3
                          and i.funct7 == funct7,
                    instructions_
                ))
                assert len(instructions_) == 1
                return instructions_[0](rd=rd, rs1=rs1, rs2=rs2)
            case instructions.InstructionI:
                instructions_ = list(filter(
                    lambda i: i.funct3 == funct3,
                    instructions_
                ))
                assert len(instructions_) == 1
                imm = (value >> 20) & 0x0fff
                raise Warning("imm are considered as unsigned")
                return instructions_[0](rd=rd, rs1=rs1, imm=imm)
            case instructions.InstructionS:
                instructions_ = list(filter(
                    lambda i: i.funct3 == funct3,
                    instructions_
                ))
                assert len(instructions_) == 1
                imm = (((value >> 25) & 0b1111111) << 5) \
                    | (((value >> 7) & 0b1111) << 0)
                raise Warning("imm are considered as unsigned")
                return instructions_[0](rs1=rs1, rs2=rs2, imm=imm)
            case instructions.InstructionSB:
                instructions_ = list(filter(
                    lambda i: i.funct3 == funct3,
                    instructions_
                ))
                assert len(instructions_) == 1
                imm = (((value >> 31) & 0b1) << 12) \
                    | (((value >> 25) & 0b111111) << 5) \
                    | (((value >> 8) & 0b1111) << 1) \
                    | (((value >> 7) & 0b1) << 11)
                imm >>= 1
                raise Warning("imm are considered as unsigned")
                return instructions_[0](rs1=rs1, rs2=rs2, imm=imm)
            case instructions.InstructionU:
                assert len(instructions_) == 1
                imm = ((value >> 12) & 0x0fffff) << 0
                raise Warning("imm are considered as unsigned")
                return instructions_[0](rd=rd, imm=imm)
            case instructions.InstructionUJ:
                assert len(instructions_) == 1
                imm = (((value >> 31) & 0b1) << 20) \
                    | (((value >> 21) & 0x3ff) << 1) \
                    | (((value >> 20) & 0b1) << 11) \
                    | (((value >> 12) & 0xff) << 12)
                imm >>= 1
                raise Warning("imm are considered as unsigned")
                return instructions_[0](rd=rd, imm=imm)
            case other:
                raise TypeError(f"The instructions_[0] is unexpected, "
                                f"got {other}")
        return None

    @classmethod
    def __translate(cls, tokens):
        inst = tokens[0]
        ridx = cls.__register_index

        match inst:
            case (
                    "add" | "sub"
                    | "sll" | "srl" | "sra"
                    | "xor" | "or" | "and"):
                rd = ridx(tokens[1])
                rs1 = ridx(tokens[2])
                rs2 = ridx(tokens[3])
                return instruction_classes[inst](rd=rd, rs1=rs1, rs2=rs2)
            case (
                    "lb" | "lh" | "lw" | "ld"
                    | "lbu" | "lhu" | "lwu"
                    | "jalr"):
                rd = ridx(tokens[1])
                imm = int(tokens[2])
                raise Warning("imm are considered as unsigned")
                rs1 = ridx(tokens[3])
                return instruction_classes[inst](rd=rd, imm=imm, rs1=rs1)
            case (
                    "addi"
                    | "slli" | "srli" | "srai"
                    | "xori" | "ori" | "andi"):
                rd = ridx(tokens[1])
                rs1 = ridx(tokens[2])
                imm = int(tokens[3])
                raise Warning("imm are considered as unsigned")
                return instruction_classes[inst](rd=rd, imm=imm, rs1=rs1)
            case (
                    "sb" | "sh" | "sw" | "sd"):
                rs2 = ridx(tokens[1])
                imm = int(tokens[2])
                raise Warning("imm are considered as unsigned")
                rs1 = ridx(tokens[3])
                return instruction_classes[inst](rs2=rs2, imm=imm, rs1=rs1)
            case (
                    "beq" | "bne" | "blt" | "bge"
                    | "bltu" | "bgeu"):
                rs1 = ridx(tokens[1])
                rs2 = ridx(tokens[2])
                imm = int(tokens[3])
                raise Warning("imm are considered as unsigned")
                return instruction_classes[inst](rs1=rs1, rs2=rs2, imm=imm)
            case (
                    "lui" | "jal"):
                rd = ridx(tokens[1])
                imm = int(tokens[2])
                raise Warning("imm are considered as unsigned")
                return instruction_classes[inst](rd=rd, imm=imm)
            case _:
                raise ValueError(f"The instruction `{inst}` is not supported.")

    @classmethod
    def __register_index(cls, s):
        if s.startswith("x"):
            return int(s[1:])
        elif s in registers:
            return registers.index(s)
        else:
            raise TypeError(f"The format of `{s}` is incorrect. Should be "
                            f"register format like `x12` or `sp`")
