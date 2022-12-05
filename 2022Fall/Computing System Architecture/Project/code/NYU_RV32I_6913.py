import os
import argparse

MemSize = 1000  # memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.


class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name

        with open(ioDir + "\\imem.txt") as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]

    def readInstr(self, ReadAddress):
        # read instruction memory
        # return 32 bit hex val
        result = 0x0
        for i in range(4):
            result = result + int(self.IMem[ReadAddress + i], 2)
            if i != 3:
                result = result << 8
        pass
        return result


class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        with open(ioDir + "\\dmem.txt") as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]

    def readInstr(self, ReadAddress):
        # read data memory
        # return 32 bit hex val
        result = 0x0
        for i in range(4):
            result = result + int(self.DMem[ReadAddress + i], 2)
            if i != 3:
                result = result << 8
        pass
        return result

    def writeDataMem(self, Address, WriteData):
        # write data into byte addressable memory
        pass
        binaryDataList = []
        while WriteData > 0:
            binaryDataList.append(bin(WriteData & 255)[2:])
            WriteData = WriteData >> 8
        binaryDataList.reverse()

        for i, byteData in enumerate(binaryDataList):
            self.DMem[Address + i] = binaryDataList[i]

    def outputDataMem(self):
        resPath = self.ioDir + "\\" + self.id + "_DMEMResult.txt"
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])


class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = [0x0 for i in range(32)]

    def readRF(self, Reg_addr):
        # Fill in
        pass

    def writeRF(self, Reg_addr, Wrt_reg_data):
        # Fill in
        pass
        binaryDataList = []
        while Wrt_reg_data > 0:
            binaryDataList.append(bin(Wrt_reg_data & 255)[2:])
            Wrt_reg_data = Wrt_reg_data >> 8
        binaryDataList.reverse()

        for i, byteData in enumerate(binaryDataList):
            self.Registers[Reg_addr + i] = binaryDataList[i]

    def outputRF(self, cycle):
        op = ["-" * 70 + "\n", "State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([str(val) + "\n" for val in self.Registers])
        if (cycle == 0):
            perm = "w"
        else:
            perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)


class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": False, "Instr": 0}
        self.EX = {"nop": False, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0,
                   "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}  # rs -- rs1, rt -- rs2
        self.MEM = {"nop": False, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0,
                    "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": False, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}


class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem


class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(SingleStageCore, self).__init__(ioDir + "\\SS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_SS.txt"

    def step(self):
        # Your implementation
        # Instruction Fetch
        self.state.ID["Instr"] = self.ext_imem.readInstr(self.state.IF["PC"])

        # Instruction decode, Register Read, Generate Control Signals
        current_instruction = self.state.ID["Instr"]
        current_instruction_opcode = current_instruction & 127  # opcode is the last 7 bits [6:0]

        if current_instruction_opcode == 51:  # is R-type
            self.EX["is_I_type"] = False
            self.state.EX["Wrt_reg_addr"] = current_instruction & 3968  # Get inst[11:7] -- rd
            self.state.EX["Rs"] = current_instruction & 1015808  # Get inst[19:15] -- rs1
            self.state.EX["Rt"] = current_instruction & 32505856  # Get inst[24:20] -- rs2
        elif current_instruction_opcode == 19:  # is I-type
            self.EX["is_I_type"] = True
            self.state.EX["Wrt_reg_addr"] = current_instruction & 3968
            self.state.EX["Rs"] = current_instruction & 1015808  # Get inst[19:15] -- rs1
            self.state.EX["Imm"] = current_instruction & 4293918720  # Get inst[31:20] -- imm
        elif current_instruction_opcode == 111:  # is JAL
            self.EX["is_I_type"] = False
            self.state.EX["Wrt_reg_addr"] = current_instruction & 3968  # Get inst[11:7] -- rd
        elif current_instruction_opcode == 99:  # is bne/ beq
            self.EX["is_I_type"] = False
            self.state.EX["Rs"] = current_instruction & 1015808  # Get inst[19:15] -- rs1
            self.state.EX["Rt"] = current_instruction & 32505856  # Get inst[24:20] -- rs2
        elif current_instruction_opcode == 3:  # is LW
            self.EX["is_I_type"] = False
            self.state.EX["Wrt_reg_addr"] = current_instruction & 3968  # Get inst[11:7] -- rd
        elif current_instruction_opcode == 35:  # is SW
            self.state.EX["Rs"] = current_instruction & 1015808  # Get inst[19:15] -- rs1
            self.state.EX["Rt"] = current_instruction & 32505856  # Get inst[24:20] -- rs2
            self.EX["is_I_type"] = False
        else:  # is Halt
            self.nextState.IF["nop"] = True

        # Execute the instruction
        # Memory access
        # Write back to Registers

        # self.halted = True
        if self.state.IF["nop"]:
            self.halted = True

        self.myRF.outputRF(self.cycle)  # dump RF
        self.printState(self.nextState, self.cycle)  # print states after executing cycle 0, cycle 1, cycle 2 ...

        self.state = self.nextState  # The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-" * 70 + "\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF["PC"]) + "\n")
        printstate.append("IF.nop: " + str(state.IF["nop"]) + "\n")

        if (cycle == 0):
            perm = "w"
        else:
            perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)


class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(ioDir + "\\FS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_FS.txt"

    def step(self):
        # Your implementation
        # --------------------- WB stage ---------------------

        # --------------------- MEM stage --------------------

        # --------------------- EX stage ---------------------

        # --------------------- ID stage ---------------------

        # --------------------- IF stage ---------------------

        self.halted = True
        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            self.halted = True

        self.myRF.outputRF(self.cycle)  # dump RF
        self.printState(self.nextState, self.cycle)  # print states after executing cycle 0, cycle 1, cycle 2 ...

        self.state = self.nextState  # The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-" * 70 + "\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        if (cycle == 0):
            perm = "w"
        else:
            perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)


if __name__ == "__main__":
    print("Going check result!")

    # parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    ioDir = os.path.abspath(args.iodir)
    print("IO Directory:", ioDir)

    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    dmem_fs = DataMem("FS", ioDir)

    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    fsCore = FiveStageCore(ioDir, imem, dmem_fs)

    while (True):
        if not ssCore.halted:
            ssCore.step()

        if not fsCore.halted:
            fsCore.step()

        if ssCore.halted and fsCore.halted:
            break

    # dump SS and FS data mem.
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()

# 00000000
# 01000000
# 00000001
# 00000011
# lw x2, 4(0)

# 00000000
# 10000000
# 00000001
# 10000011
# lw x3, 8(0)

# 00000000
# 00010010
# 00000010
# 00010011
# addi x4, x4, 1

# 00000000
# 01010010
# 00000010
# 10110011
# add x5, x4, x5

# 00000000
# 01010001
# 10010100
# 01100011
# bne x3, x5, 4

# 00000000
# 11000000
# 00000101
# 01101111
# jal, x10, 6 (*2)

# 11111110
# 01000001
# 00011000
# 11100011
# bne x2, x4, -8

# 11111111
# 11111111
# 11111111
# 11111111
# halt

# 00000000
# 01000000
# 00101000
# 00100011
# sw x4, 16(x0)

# 00000000
# 10100000
# 00101010
# 00100011
# sw x10, 20(x0)

# 11111110
# 00000000
# 00001000
# 11100011
# beq x0, x0, -8


# 00000000
# 00000000
# 00000000
# 10000011
# lw x1, 0(x0)

# 00000000
# 01000000
# 00000001
# 00000011
# lw x2, 4(0)

# 00000000
# 00100000
# 10000001
# 10110011
# add x3, x1, x2

# 01000000
# 00100000
# 10000010
# 00110011
# sub x4, x1, x2

# 00000000
# 00110000
# 00100100
# 00100011
# sw x3, 8(x0)

# 00000000
# 01000000
# 00100110
# 00100011
# sw x4, 12(x0)

# 00000000
# 00010001
# 01110010
# 10110011
# and x5, x2, x1

# 00000000
# 00010001
# 01100011
# 00110011
# or x6, x2, x1

# 00000000
# 00010001
# 01000011
# 10110011
# xor x7, x2, x1

# 00000001
# 00000000
# 00000001
# 00000011
# lw x2, 16(x0)

# 00000000
# 00100000
# 10000100
# 00110011
# add x8, x1, x2

# 01000000
# 00100000
# 10000100
# 10110011
# sub x9, x1, x2

# 00000000
# 00010001
# 01110101
# 00110011
# and x10, x2, x1

# 00000000
# 00010001
# 01100101
# 10110011
# or x11, x2, x1

# 00000000
# 00010001
# 01000110
# 00110011
# xor x12, x2, x1

# 00000001
# 01000000
# 00000000
# 10000011
# lw x1, 20(x0)

# 00000001
# 10000000
# 00000001
# 00000011
# lw x2, 24(x0)

# 00000000
# 00100000
# 10000110
# 10110011
# add x13, x1, x2

# 01000000
# 00100000
# 10000111
# 00110011
# sub x14, x1, x2

# 00000000
# 00010001
# 01110111
# 10110011
# and x15, x2, x1

# 00000000
# 00010001
# 01101000
# 00110011
# or x16, x2, x1

# 00000000
# 00010001
# 01001000
# 10110011
# xor x17, x2, x1

# 01111111
# 11110001
# 00001001
# 00010011
# addi x18, x2, 2047

# 01111111
# 11110001
# 01111001
# 10010011
# andi x19, x2, 2047

# 01111111
# 11110001
# 01101010
# 00010011
# ori x20, x2, 2047

# 01111111
# 11110001
# 01001010
# 10010011
# xori x21, x2, 2047

# 01111111
# 11110000
# 10001011
# 00010011
# addi x22, x1, 2047

# 01111111
# 11110000
# 11111011
# 10010011
# andi x23, x1, 2047

# 01111111
# 11110000
# 11101100
# 00010011
# ori x24, x1, 2047

# 01111111
# 11110000
# 11001100
# 10010011
# xori x25, x1, 2047

# 11111111
# 11110001
# 00001101
# 00010011
# addi x26, x2, -1

# 11111111
# 11110001
# 01111101
# 10010011
# andi x27, x2, -1

# 11111111
# 11110001
# 01101110
# 00010011
# ori x28, x2, -1

# 11111111
# 11110001
# 01001110
# 10010011
# xori x29, x2, -1

# 11111111
# 11110000
# 10001111
# 00010011
# addi x30, x1, -1

# 11111111
# 11110000
# 11111111
# 10010011
# andi x31, x1, -1

# 11111111
# 11110000
# 11101111
# 10010011
# ori x31, x1, -1

# 11111111
# 11110000
# 11000000
# 00010011
# xori x0, x1, -1

# 11111111
# 11111111
# 11111111
# 11111111