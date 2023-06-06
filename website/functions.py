def extract_fields(inst):
    body = inst.body
    parts = body.replace(',', '').split()
    if parts[0] in ["NAND", "ADDI", "ADD", "SLL", "NEG"]:

        inst.type = parts[0]
        assert (int(parts[1][1:]) in range(0, 8))
        assert (int(parts[2][1:]) in range(0, 8))
        if parts[0] == "ADDI":
            inst.des = int(parts[1][1:])
            inst.s1 = int(parts[2][1:])
            assert (int(parts[3]) in range(-64, 63))
            inst.offset = int(parts[3])
        elif parts[0] == "NEG":
            inst.des = int(parts[1][1:])
            inst.s1 = int(parts[2][1:])
        else:
            assert (int(parts[3][1:]) in range(0, 8))
            inst.des = int(parts[1][1:])
            inst.s1 = int(parts[2][1:])
            inst.s2 = int(parts[3][1:])

    elif parts[0] in ["STORE", "LOAD"]:
        LS_instruction = body.replace('(', ' ').split()
        LS_instruction = [word.replace(',', '').replace('(', '').replace(')', '') for word in LS_instruction]
        if LS_instruction[0] == "STORE":
            inst.type = LS_instruction[0]
            inst.s1 = int(LS_instruction[1][1])
            inst.s2 = int(LS_instruction[3][1])
            inst.offset = int(LS_instruction[2])
        else:
            inst.type = LS_instruction[0]
            inst.des = int(LS_instruction[1][1])
            inst.s1 = int(LS_instruction[3][1])
            inst.offset = int(LS_instruction[2])

    elif parts[0] == "BNE":
        BNE_instruction = body.split()
        BNE_instruction = [word.replace(',', '') for word in BNE_instruction]
        inst.type = BNE_instruction[0]
        inst.s1 = int(BNE_instruction[1][1])
        inst.s2 = int(BNE_instruction[2][1])
        inst.offset = int(BNE_instruction[3])
    elif parts[0] == "JAL":
        JAL_instruction = body.split()
        JAL_instruction = [word.replace(',', '') for word in JAL_instruction]
        inst.type = JAL_instruction[0]
        inst.offset = int(JAL_instruction[1])
    elif parts[0] == "RET":
        inst.type = "RET"
    else:
        print("Error: Instruction is wrong")
        assert ()


def No_Pending_exe(RSs):
    for RS in RSs.list:
        if RS.busy:
            # print("Still exec" + RS.name)
            return False

    return True
