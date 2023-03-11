# Nicholas Lee
# COMP3971 Winter 2023

import struct
import os

TEXT_OFFSET = 128
TEXT_SIZE = 0
DATA_OFFSET = 0
DATA_SIZE = 0

def disassemble_instruction(instr):
    opcode = instr[25:]
    rd = int(instr[20:25],2)
    funct3 = instr[17:20]
    rs1 = int(instr[12:17],2)
    rs2 = int(instr[7:12],2)
    funct7 = instr[:7]
    imm_i = int(instr[0:12],2)
    imm_s = int(instr[:7]+instr[20:25],2)
    imm_sb = int(instr[:7]+instr[20:25]+"0",2)

    # R: f"ins x{rd}, x{rs1}, x{rs2}" # INS(R)
    # I: f"ins x{rd}, x{rs1}, {imm_i}" # INS(I)
    # S: f"ins x{rs2}, ({imm_s})x{rs1}" # INS(S)
    # SB: f"ins x{rs1}, x{rs2}, {imm_sb}" # INS(SB)

    if opcode == "0000011":
        return f"lw x{rd}, x{rs1}, {imm_i}" # lw(I)
    elif opcode =="0010011":
        if funct3 == "000":
            return f"addi x{rd}, x{rs1}, {imm_i}" # ADDI(I)
        elif funct3 == "001":
            return f"slli x{rd}, x{rs1}, {imm_i}" # SLLI(I)
    elif opcode =="0100011":
        return f"sw x{rs2}, ({imm_s})x{rs1}" # SW(S)
    elif opcode =="0110011":
        if funct3 == "000":
            if funct7 == "0000000":
                return f"add x{rd}, x{rs1}, x{rs2}" # ADD(R)
            elif funct7 == "0100000":
                return f"sub x{rd}, x{rs1}, x{rs2}" # SUB(R)
        elif funct3 == "111":
            return f"and x{rd}, x{rs1}, x{rs2}" # AND(R)
    elif opcode =="1100011":
        if funct3 == "000":
            return f"beq x{rs1}, x{rs2}, {imm_sb}" # BEQ(SB)
        elif funct3 == "100":
            return f"blt x{rs1}, x{rs2}, {imm_sb}" # BLT(SB)
        elif funct3 == "101":
            return f"bge x{rs1}, x{rs2}, {imm_sb}" # BGE(SB)
    elif opcode =="1100111":
        return f"jalr x{rd}, x{rs1}, {imm_i}" # jalr(I)
    elif opcode =="1110011":
        return f"ecall x{rd}, x{rs1}, {imm_i}" # ECALL(I)
    return "UNKNOWN INSTRUCTION"

    
def disassemble(filename):
    # Open the binary file in binary mode
    with open(filename, "rb") as file:
        # find size of .text segment
        file.seek(64+16)
        data = file.read(4)
        TEXT_SIZE = int.from_bytes(data, byteorder='little')

        # Find offset of .data segment
        file.seek(96+4)
        data = file.read(4)
        DATA_OFFSET= int.from_bytes(data, byteorder='little')

        # Find size of .data segment
        file.seek(96+16)
        data = file.read(4)
        DATA_SIZE = int.from_bytes(data, byteorder='little')

        #print
        print("Text Offset: ",TEXT_OFFSET)
        print("Text Size: ",TEXT_SIZE)
        print("Data Offset: ",DATA_OFFSET)
        print("Data Size: ",DATA_SIZE)

        print(".text")
        for x in range(int(TEXT_SIZE/4)):
            #Find current instruction to decode
            file.seek(TEXT_OFFSET+(x*4))
            data = file.read(4)

            #Convert to binary
            integer_data = struct.unpack('<I', data)[0]
            binary_data = bin(integer_data)[2:].zfill(32)

            #Print formatted disassembled data
            print ("{:<10} {:<10} {:<10}".format('{:08d}'.format(x*4)+":", hex(integer_data)[2:].zfill(8), disassemble_instruction(binary_data)))

        print(".data")
        for y in range(int(DATA_SIZE/4)):
            #Find current instruction to decode
            file.seek(DATA_OFFSET+(y*4))
            data = file.read(4)

            #Convert to integer
            integer_data = struct.unpack('<I', data)[0]

            #Print data segment
            print ("{:<10} {:<10}".format('{:08d}'.format((y*4)+TEXT_SIZE)+":", hex(integer_data)[2:].zfill(8)))

if __name__ == "__main__":

    #Main loop to parse files till user is finished
    done = False
    while(not done):
        filename = input("Please Enter Filename: ")
        if os.path.isfile(filename):
            disassemble(filename)
            resp = input("Would you like to enter another file? (y/n): ")
            if(resp.lower() == "n"):
                done = True
        else:
            print("Invalid File! Please try again...")

          