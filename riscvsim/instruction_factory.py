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
        tokens = __class__.__extract_tokens(x)
        instruction = __class__.__translate(tokens)
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

        text = [__class__.get(_) for _ in text]
        return text

    @classmethod
    def __extract_tokens(cls, x):
        if isinstance(x, int):
            # TODO: imlement, test
            raise NotImplementedError
        elif isinstance(x, str):
            tokens = x.lower() \
                .replace(",", " ") \
                .replace("(", " ") \
                .replace(")", " ") \
                .split()
        else:
            raise TypeError(f"The x should be 'int' or 'str', "
                            f"got {type(x)}")
        return tokens

    @classmethod
    def __translate(cls, tokens):
        inst = tokens[0]
        ridx = __class__.__register_index

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
                rs = ridx(tokens[3])
                return instruction_classes[inst](rd=rd, imm=imm, rs=rs)
            case (
                    "addi"
                    | "slli" | "srli" | "srai"
                    | "xori" | "ori" | "andi"):
                rd = ridx(tokens[1])
                rs = ridx(tokens[2])
                imm = int(tokens[3])
                return instruction_classes[inst](rd=rd, imm=imm, rs=rs)
            case (
                    "sb" | "sh" | "sw" | "sd"):
                rs2 = ridx(tokens[1])
                imm = int(tokens[2])
                rs1 = ridx(tokens[3])
                return instruction_classes[inst](rs2=rs2, imm=imm, rs1=rs1)
            case (
                    "beq" | "bne" | "blt" | "bge"
                    | "bltu" | "bgeu"):
                rs1 = ridx(tokens[1])
                rs2 = ridx(tokens[2])
                imm = int(tokens[3])
                return instruction_classes[inst](rs1=rs1, rs2=rs2, imm=imm)
            case (
                    "lui" | "jal"):
                rd = ridx(tokens[1])
                imm = int(tokens[2])
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
