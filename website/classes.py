from .functions import extract_fields
import array


class instruction:
    def __init__(self, body):
        self.body = body
        self.is_issued = None
        self.is_executed = None
        self.is_wrote = None
        self.issue_start_time = None
        self.execute_start_time = None
        self.write_start_time = None
        self.issue_end_time = None
        self.execute_end_time = None
        self.write_end_time = None
        self.type = None
        self.des = None
        self.s1 = None
        self.s2 = None
        self.offset = None
        parts = extract_fields(self)

    def print(self):
        if self.type == "STORE":
            print(self.type + " R" + str(self.s1) + " " + str(self.offset) + " (R" + str(self.s2) + ")")
        elif self.type == "LOAD":
            print(self.type + " R" + str(self.des) + " " + str(self.offset) + " (R" + str(self.s1) + ")")
        elif self.type == "BNE":
            print(self.type + " R" + str(self.s1) + " R" + str(self.s2) + " " + str(self.offset))

        elif self.type == "JAL":
            print(self.type + " " + str(self.offset))
        elif self.type == "RET":
            print(self.type)
        elif self.type == "ADDI":
            print(self.type + " R" + str(self.des) + " R" + str(self.s1) + " " + str(self.offset))
        elif self.type == "NEG":
            print(self.type + " R" + str(self.des) + " R" + str(self.s1))
        else:
            print(self.type + " R" + str(self.des) + " R" + str(self.s1) + " R" + str(self.s2))


class memory:
    def __init__(self):
        self.memory = array.array('h', [0] * (2 ** 16))

    def write(self, location, data):
        assert (location in range(0, 65536))
        assert (data in range(-32768, 32767))
        self.memory[location] = data

    def read(self, location):
        assert (location in range(0, 65536))
        return self.memory[location]


class instructions_q:
    def __init__(self, pc):
        self.pc = pc
        self.queue = []

    def insert(self, inst):
        self.queue.append(inst)
        self.pc += 1

    def __len__(self):
        return len(self.queue)

    def pop(self):
        return self.queue.pop()

    def print_insts(self):
        print("---Instructions------")
        for i in self.queue:
            i.print()
        print("__________________")


class register:
    def __init__(self, num):
        self.num = num
        self.data = 0
        self.Q = ""


class registers:
    def __init__(self):
        self.list = [register(i) for i in range(8)]

    def __getitem__(self, item):
        return self.list[item]

    def print_registers(self):
        print("---Registers------")
        for i in self.list:
            print("Register", i.num, i.data, i.Q)
        print("__________________")

    def write_register(self, idx, value):
        assert (idx in range(1, 8))
        self.list[idx].data = value

    def read_register(self, idx):
        assert (idx in range(0, 8))
        return self.list[idx].data


def format_attribute(attribute):
    return str(attribute) if attribute is not None else ""


class Reservation_Station:
    def __init__(self, name, num):
        self.name = name
        self.busy = False
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.numcycles = num
        self.remaining = num
        self.value_to_write = ""
        self.is_executed = False
        self.pc = None
        self.target = None
        self.inst = None
        self.branch_is_handeled = False

    def clear(self):
        self.busy = False
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.remaining = self.numcycles
        self.value_to_write = ""
        self.is_executed = False
        self.pc = None
        self.target = None
        self.inst = None
        self.branch_is_handeled= False

    def print_reservation_station(self):
        print("Reservation Station: {}".format(self.name))
        print("+--------+-------+-----+-----+-----+-----+-----+")
        print("|  Busy  |  OP   |  Vj |  Vk |  Qj |  Qk |  A  |")
        print("+--------+-------+-----+-----+-----+-----+-----+")
        print("|  {:<5} | {:<5} | {:<3} | {:<3} | {:<3} | {:<3} | {:<3} |".format(
            format_attribute(self.busy), format_attribute(self.op), format_attribute(self.Vj),
            format_attribute(self.Vk), format_attribute(self.Qj), format_attribute(self.Qk),
            format_attribute(self.A)))
        print("+--------+-------+-----+-----+-----+-----+-----+")


class Reservation_Stations:
    def __init__(self):
        self.list = []
        self.list.append(Reservation_Station("LOAD", 2))
        self.list.append(Reservation_Station("LOAD1", 2))
        self.list.append(Reservation_Station("STORE", 2))
        self.list.append(Reservation_Station("STORE1", 2))
        self.list.append(Reservation_Station("BNE", 1))
        self.list.append(Reservation_Station("JAL/RET ", 1))
        self.list.append(Reservation_Station("ADD/ADDI", 2))
        self.list.append(Reservation_Station("ADD/ADDI1", 2))
        self.list.append(Reservation_Station("ADD/ADDI2", 2))
        self.list.append(Reservation_Station("NEG", 2))
        self.list.append(Reservation_Station("NAND", 1))
        self.list.append(Reservation_Station("SLL", 8))

    def print(self):
        print("---Reservation_Stations------")
        for i in self.list:
            print("station", i.name, i.numcycles)
        print("__________________")

    def search(self, name):
        for i in self.list:
            if name in i.name and i.busy is False:
                return i
        return None
