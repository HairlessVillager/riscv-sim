from .config import REGISTERS_DIR, SIZE


class Register:
    # TODO: tests are required

    def __init__(self, bytes_num, value=0):
        self.bytes_num = bytes_num
        self.value = value

    def get(self, bytes_num, *, signed):
        # TODO: type check, test is required
        value = self.value & ((1 << (bytes_num*8)) - 1)
        if signed and value & (1 << (bytes_num*8 - 1)):
            value -= 1 << (bytes_num * 8)
        return value

    def set(self, bytes_num, value):
        # TODO: type check, test is required
        if not isinstance(bytes_num, int):
            raise TypeError(f"The 'bytes_num' should be 'int', "
                            f"got {type(bytes_num)}.")
        if not (bytes_num > 0):
            raise ValueError(f"The 'bytes_num' should be > 0, "
                             f"got {bytes_num}.")
        if not isinstance(value, int):
            raise TypeError(f"The 'value' should be 'int', "
                            f"got {type(bytes_num)}.")
        bytes_num = min(bytes_num, self.bytes_num)
        down_bound = -(1 << (bytes_num * 8 - 1))
        up_bound = +(1 << (bytes_num * 8))
        if not (down_bound <= value < up_bound):
            raise ValueError(f"The 'value' should be "
                             f"{down_bound} <= value < {up_bound}, "
                             f"got {value}.")
        if value < 0:
            value += 1 << (bytes_num * 8)
        self.value = value & ((1 << (bytes_num*8)) - 1)

    def __str__(self):
        return hex(self.value)

    def __repr__(self):
        return f"<{__class__.__name__} {self.bytes_num}B {str(self)}>"

    def copy(self):
        register = Register(bytes_num=self.bytes_num, value=self.value)
        return register

class Registers:

    def __init__(self, *args, **kwargs):
        # TODO: fix the hardcode
        object.__setattr__(self, "len_", 32)
        object.__setattr__(self, "values", [Register(SIZE) for _ in range(self.len_)])
        for i, arg in enumerate(args):
            x = self.__getitem__(i)
            x.set(SIZE, arg)
        for kw, arg in kwargs.items():
            x = self.__getitem__(REGISTERS_DIR[kw])
            x.set(SIZE, arg)

    def __getitem__(self, register):
        if isinstance(register, int):
            return self.values[register]
        elif isinstance(register, str):
            return self.values[REGISTERS_DIR[register]]
        else:
            raise TypeError(f"The 'register' should be 'int' or 'str', "
                            f"got {type(register)}.")

    def __str__(self):
        s = [f"{'x'+str(i):>3} "
             f"{v.get(SIZE, signed=False):=20} "
             f"{v.get(SIZE, signed=False):0=#18x}"
             for i, v in enumerate(self.values)]
        return f"{__class__.__name__}:\n" + "\n".join(s)

    def copy(self):
        registers = Registers()
        registers.values = [_.copy() for _ in self.values]
        return registers


class Memory:

    def __init__(self, addr_max=0xffffffff):
        self.addr_max = addr_max
        self.values = {}

    def __len__(self):
        return size

    def __getitem__(self, addr):
        if addr not in self.values:
            self.values[addr] = Register(1, 0x00)
        return self.values[addr]

    def read(self, addr, bytes_num, *, signed):
        # TODO: type check
        value = 0
        for i in reversed(range(bytes_num)):
            value <<= 8
            value += self.values[addr + i].get(1, signed=False)
        if signed and value & (1 << (bytes_num*8 - 1)):
            value -= 1 << (bytes_num * 8)
        return value

    def write(self, addr, bytes_num, value):
        # TODO: type check
        for i in range(bytes_num):
            self.values[addr + i] = Register(1, value & 0xff)
            value >>= 8

    def __str__(self):
        addrs_x8 = sorted(list(set(_ & ~0x07 for _ in self.values.keys())))
        if addrs_x8:
            s = []
            last_addr_x8 = None

            for addr_x8 in addrs_x8:
                if last_addr_x8 and addr_x8 != last_addr_x8 + 8:
                    s.append("...")
                xs = []
                for i in range(addr_x8, addr_x8 + 8):
                    if i in self.values:
                        xs.append(f"{self[i].get(1, signed=False):0=2x}")
                    else:
                        xs.append("..")
                s.append(
                    f"{addr_x8:0=#10x}  "
                    f"{' '.join(xs[:4])}   {' '.join(xs[4:])}")
                last_addr_x8 = addr_x8

            return f"{__class__.__name__}:\n" + "\n".join(s)
        else:
            return f"{__class__.__name__} is empty."

    def copy(self):
        memory = Memory()
        memory.values = {k: v.copy() for k, v in self.values.items()}
        return memory


class Simulator:

    def __init__(self, **kwargs):
        object.__setattr__(self, "registers", Registers())
        object.__setattr__(self, "memory", Memory())
        object.__setattr__(self, "pc", 0)

        for kw, arg in kwargs.items():
            # TODO: add test for the code below
            try:
                self.__setattr__(kw, arg)
            except KeyError:
                raise TypeError(f"The keyword '{kw}' is not supported.")

    # shortcut for registers/memory access
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.memory[key].set(1, value)
        elif isinstance(key, str):
            self.__setattr__(key, value)
        else:
            raise TypeError(f"The 'key' should be 'int' or 'str', "
                            f"got {type(key)}")

    # shortcut for registers/memory access
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.memory[key].get(1, signed=False)
        elif isinstance(key, str):
            return self.__getattr__(key)
        else:
            raise TypeError(f"The 'key' should be 'int' or 'str', "
                            f"got {type(key)}")

    # shortcut for registers access
    def __setattr__(self, name, value):
        if name in dir(self):
            object.__setattr__(self, name, value)
        else:
            self.registers[name].set(SIZE, value)

    # shortcut for registers access
    def __getattr__(self, name):
        try:
            return self.registers[name].get(SIZE, signed=False)
        except KeyError:
            raise AttributeError(f"The attribute '{name}' was not found "
                            f"both in Simulator and Registers.")

    def set_memory(self, values=(), start=0, bytes_num=1):
        for i, v in enumerate(values):
            self.memory[start+i].set(1, v)

    def step(self, instruction=None):
        if isinstance == None:
            # TODO
            pass
        else:
            instruction.run_by(self)

    def __str__(self):
        return "\n".join([
            f"{__class__.__name__} Info",
            "=" * 43,
            f"pc={self.pc} {self.pc:#x}",
            str(self.registers),
            str(self.memory),
        ])

    def copy(self):
        sim = Simulator()
        sim.pc = self.pc
        sim.registers = self.registers.copy()
        sim.memory = self.memory.copy()
        return sim

