from .classes import memory, instruction, registers, Reservation_Stations, instructions_q, Reservation_Station
from collections import deque

global branch_flag
branch_flag = False

global Branch_RS
Branch_RS = None


def issue(RS: Reservation_Station, inst: instruction, regs: registers, Load_store_queue: deque,
          current_clock_cycle, pc):
    # inst.print()

    if inst.type == "LOAD":
        if regs[int(inst.s1)].Q != "":
            RS.Qj = regs[inst.s1].Q
        else:
            RS.Vj = regs[int(inst.s1)].data

        RS.A = inst.offset
        RS.busy = True
        regs[int(inst.des)].Q = RS.name
        RS.op = inst.type
        Load_store_queue.append(RS.name)

    elif inst.type == "STORE":
        if regs[int(inst.s2)].Q != "":
            RS.Qj = regs[int(inst.s2)].Q
        else:
            RS.Vj = regs[int(inst.s2)].data

        if regs[int(inst.s1)].Q != "":
            RS.Qk = regs[int(inst.s1)].Q
        else:
            RS.Vk = regs[int(inst.s1)].data
            RS.Qk = None
        RS.op = inst.type
        RS.A = inst.offset
        RS.busy = True
        Load_store_queue.append(RS.name)
    elif inst.type in ["NAND", "ADD", "SLL"]:
        if regs[inst.s1].Q != "":
            RS.Qj = regs[int(inst.s1)].Q
        else:
            RS.Vj = regs[int(inst.s1)].data

        if regs[inst.s2].Q != "":
            RS.Qk = regs[int(inst.s2)].Q
        else:
            RS.Vk = regs[int(inst.s2)].data

        RS.busy = True
        regs[int(inst.des)].Q = RS.name
        RS.op = inst.type
    elif inst.type == "NEG":
        if regs[inst.s1].Q != "":
            RS.Qj = regs[int(inst.s1)].Q
        else:
            RS.Vj = regs[int(inst.s1)].data

        RS.busy = True
        regs[int(inst.des)].Q = RS.name
        RS.op = inst.type

    elif inst.type == "ADDI":
        if regs[inst.s1].Q != "":
            RS.Qj = regs[int(inst.s1)].Q
        else:
            RS.Vj = regs[int(inst.s1)].data

        RS.A = inst.offset
        RS.busy = True
        regs[int(inst.des)].Q = RS.name
        RS.op = inst.type

    elif inst.type == "JAL":

        RS.busy = True
        regs[1].Q = RS.name
        RS.op = inst.type
        RS.branch_is_handeled = False
        RS.A = inst.offset
    elif inst.type == "RET":
        if regs[1].Q != "":
            RS.Qj = regs[1].Q
        else:
            RS.Vj = regs[1].data
        RS.busy = True
        regs[1].Q = RS.name
        RS.op = inst.type
        RS.value_to_write = inst.offset
        RS.branch_is_handeled = False
    elif inst.type == "BNE":

        if regs[inst.s1].Q != "":
            RS.Qj = regs[int(inst.s1)].Q
        else:
            RS.Vj = regs[int(inst.s1)].data

        if regs[inst.s2].Q != "":
            RS.Qk = regs[int(inst.s2)].Q
        else:
            RS.Vk = regs[int(inst.s2)].data

        RS.busy = True
        RS.op = inst.type
        RS.A = inst.offset
        RS.branch_is_handeled = False

    RS.pc = pc
    inst.is_issued = True
    inst.issue_start_time = current_clock_cycle
    RS.inst = inst


def execute(RSs: Reservation_Stations, regs: registers, mem: memory, Load_store_queue: deque, global_pc,
            current_clock_cycle):

    global branch_flag
    global Branch_RS
    for RS in RSs.list:

        if RS.busy and RS.inst.issue_start_time != current_clock_cycle:
            if RS.op == "LOAD":

                if RS.remaining == 1:

                    RS.value_to_write = mem.read(RS.A)
                    RS.is_executed = True
                    RS.inst.execute_end_time = current_clock_cycle

                elif RS.remaining == 2 and RS.Qj is None and Load_store_queue[0] == RS.name:
                    RS.A = int(RS.A) + int(RS.Vj)
                    RS.inst.execute_start_time = current_clock_cycle
                    RS.remaining -= 1

            elif RS.op == "STORE":

                if RS.remaining == 1:

                    RS.value_to_write = RS.Vk
                    RS.is_executed = True
                    RS.inst.execute_end_time = current_clock_cycle

                elif RS.remaining == 2 and RS.Qj is None and Load_store_queue[0] == RS.name:
                    RS.A = int(RS.A) + int(RS.Vj)
                    RS.remaining -= 1
                    RS.inst.execute_start_time = current_clock_cycle

            elif RS.op in ["NAND", "ADDI", "ADD", "SLL", "NEG"] and RS.Qj is None and RS.Qk is None:
                RS.busy = True
                execute_Arithmetic_Logic(RS, regs, mem, current_clock_cycle)

            elif RS.op in ["RET", "JAL", "BNE"] and RS.Qj is None and RS.Qk is None:
                if RS.op == "BNE":
                    if RS.Vj == RS.Vk:
                        RS.target = None
                    else:
                        RS.target = RS.pc + 1 + RS.A
                        branch_flag = True
                        Branch_RS = RS.name

                if RS.op == "RET":
                    RS.target = RS.Vj
                    branch_flag = True
                    Branch_RS = RS.name

                if RS.op == "JAL":
                    RS.value_to_write = RS.pc + 1
                    RS.target = RS.A
                    branch_flag = True
                    Branch_RS = RS.name

                RS.is_executed = True
                RS.inst.execute_start_time = current_clock_cycle
                RS.inst.execute_end_time = current_clock_cycle + 1


def write_back(RSs: Reservation_Stations, regs: registers, mem: memory, Load_store_queue: deque, glo_pc,
               current_clock_cycle):
    global branch_flag
    global Branch_RS
    new_PC = None
    if branch_flag:
        # print("FLag " + str(branch_flag) + str(Branch_RS))
        for RS in RSs.list:
            if RS.name == Branch_RS and RS.inst.issue_end_time != current_clock_cycle:
                for RS1 in RSs.list:
                    if RS1.busy and RS1.inst.issue_start_time > RS.inst.issue_start_time:
                        # print("Flushing " + str(RS1.name))
                        RS1.clear()
                        for r in regs:
                            if r.Q == RS1.name:
                                r.Q=""

                new_PC = RS.target
                for r in regs:
                    if r.Q == RS.name and RS.value_to_write is not None:
                        if r.num != 0:
                            r.data = RS.value_to_write
                # print("Branching to " + str(new_PC))
                RS.inst.write_start_time = current_clock_cycle
                RS.clear()
                branch_flag = False
            RS.branch_is_handeled = True

    for RS in RSs.list:
        if RS.busy and RS.inst.issue_end_time != current_clock_cycle:
            # print("Doing "+ RS.name + str(RS.branch_is_handeled))

            if RS.target is None and RS.op == "BNE" and RS.is_executed:
                RS.inst.write_start_time = current_clock_cycle
                RS.clear()

            if RS.op == "LOAD" and RS.is_executed and RS.Qk is None:
                for r in regs:
                    if r.Q == RS.name:
                        if r.num != 0:
                            r.data = RS.value_to_write
                        # print("Data wrote to " + str(r.num) + " is " + str(r.data))

                        r.Q = ""
                        Load_store_queue.popleft()
                        for resr_Station in RSs.list:
                            if resr_Station.Qj == RS.name:
                                resr_Station.Vj = RS.value_to_write
                                resr_Station.Qj = None

                            if resr_Station.Qk == RS.name:
                                resr_Station.Vk = RS.value_to_write
                                resr_Station.Qk = None
                        RS.inst.write_start_time = current_clock_cycle
                        RS.clear()
            elif RS.op == "STORE" and RS.is_executed and RS.Qk is None:
                mem.write(RS.A, RS.value_to_write)
                RS.inst.write_start_time = current_clock_cycle
                print("READ data ", mem.read(RS.A))
                Load_store_queue.popleft()
                RS.clear()

            elif RS.op in ["NAND", "ADDI", "ADD", "SLL", "NEG"] and RS.is_executed and RS.Qk is None:

                for r in regs:
                    if r.Q == RS.name:
                        if r.num != 0:
                            r.data = RS.value_to_write
                        r.Q = ""

                for resr_Station in RSs.list:
                    if resr_Station.Qj == RS.name:
                        resr_Station.Vj = RS.value_to_write
                        resr_Station.Qj = None

                    if resr_Station.Qk == RS.name:
                        resr_Station.Vk = RS.value_to_write
                        resr_Station.Qk = None
                RS.inst.write_start_time = current_clock_cycle
                RS.clear()

    return new_PC


def execute_Arithmetic_Logic(RS: Reservation_Station, regs: registers, mem: memory, current_clock_cycle):
    if RS.op in ["ADDI", "ADD", "NEG"]:
        if RS.remaining == 1:
            RS.is_executed = True
            RS.inst.execute_end_time = current_clock_cycle
        if RS.remaining == 2:
            RS.inst.execute_start_time = current_clock_cycle
            if RS.op == "ADDI":
                RS.value_to_write = int(RS.A) + int(RS.Vj)
            elif RS.op == "ADD":
                RS.value_to_write = int(RS.Vk) + int(RS.Vj)
            elif RS.op == "NEG":
                RS.value_to_write = -1 * int(RS.Vj)

            RS.remaining -= 1

    elif RS.op == "NAND":

        bin1 = bin(int(RS.Vk))[2:]
        bin2 = bin(int(RS.Vj))[2:]
        if len(bin1) > len(bin2):
            bin2 = bin(int(RS.Vj))[2:].zfill(len(bin1))
        else:
            bin1 = bin(int(RS.Vk))[2:].zfill(len(bin2))

        result = ""
        for i in range(len(bin1)):
            bit1 = int(bin1[i])
            bit2 = int(bin2[i])
            if bit1 == 1 and bit2 == 1:
                nand_bit = 0
            else:
                nand_bit = 1
            result += str(nand_bit)

        RS.value_to_write = int(result, 2)
        RS.is_executed = True
        RS.inst.execute_start_time = current_clock_cycle
        RS.inst.execute_end_time = current_clock_cycle + 1

    elif RS.op == "SLL":
        if RS.remaining == 1:
            data = bin(int(RS.Vj))[2:].zfill(16)
            result = data[1:] + "0"
            if 'b' in result:
                inx = result.find('b')
                result = result[inx + 1:]
                RS.value_to_write = int(result, 2) * -1
            else:
                RS.value_to_write = int(result, 2)
            RS.is_executed = True
            RS.inst.execute_end_time = current_clock_cycle
        else:
            if RS.remaining == RS.numcycles:
                RS.inst.execute_start_time = current_clock_cycle
            RS.remaining -= 1
