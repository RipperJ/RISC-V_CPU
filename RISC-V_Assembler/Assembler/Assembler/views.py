"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, request
from Assembler import app

inst_R = {"add": {1:"000", 2:"0000000"}, 
          "sub": {1:"000", 2:"0100000"}, 
          "sll": {1:"001", 2:"0000000"}, 
          "slt": {1:"010", 2:"0000000"}, 
          "sltu": {1:"011", 2:"0000000"},
          "xor": {1:"100", 2:"0000000"}, 
          "srl": {1:"101", 2:"0000000"}, 
          "sra": {1:"101", 2:"0100000"}, 
          "or" : {1:"110", 2:"0000000"}, 
          "and": {1:"111", 2:"0000000"}}
inst_I = {"addi": "000", 
          "slti": "010", 
          "sltiu": "011", 
          "xori": "100", 
          "ori": "110",
          "andi": "111", 
          "slli": {1: "001", 2: "0000000"}, 
          "srli": {1: "101", 2: "0000000"}, 
          "srai": {1: "101", 2: "0100000"}}
inst_L = {"lb": "000", 
          "lh": "001", 
          "lw": "010", 
          "lbu": "100", 
          "lhu": "101"}
inst_S = {"sb": "000", 
          "sh": "001",
          "sw": "010"}
inst_B = {"beq": "000",
          "bne":"001",
          "blt":"100",
          "bge":"101",
          "bltu":"110",
          "bgeu":"111"}
inst_F = {"fence", "fence.i"}
inst_EC = {"ecall", "ebreak",
           "csrrw", "csrrs", "csrrc",
           "csrrwi", "csrrsi", "csrrci"}
# lui, auipc, jal, jalr are discussed solely

def bin2comp(num):
    return (bin(((1 << 12) - 1) & num)[2:]).zfill(12)

def bin2comp20(num):
    return (bin(((1 << 20) - 1) & num)[2:]).zfill(20)

def is_imm(imm):
    try:
        eval(imm)
        return True
    except Exception:
        return False

def Reg_to_Bin(reg):
    bin_code = "$$"
    if reg == "x0" or reg == "zero":
        bin_code = "00000"
    elif reg == "x1" or reg == "ra":
        bin_code = "00001"
    elif reg == "x2" or reg == "sp":
        bin_code = "00010"
    elif reg == "x3" or reg == "gp":
        bin_code = "00011"
    elif reg == "x4" or reg == "tp":
        bin_code = "00100"
    elif reg == "x5" or reg == "t0":
        bin_code = "00101"
    elif reg == "x6" or reg == "t1":
        bin_code = "00110"
    elif reg == "x7" or reg == "t2":
        bin_code = "00111"
    elif reg == "x8" or reg == "s0" or reg == "fp":
        bin_code = "01000"
    elif reg == "x9" or reg == "s1":
        bin_code = "01001"
    elif reg == "x10" or reg == "a0":
        bin_code = "01010"
    elif reg == "x11" or reg == "a1":
        bin_code = "01011"
    elif reg == "x12" or reg == "a2":
        bin_code = "01100"
    elif reg == "x13" or reg == "a3":
        bin_code = "01101"
    elif reg == "x14" or reg == "a4":
        bin_code = "01110"
    elif reg == "x15" or reg == "a5":
        bin_code = "01111"
    elif reg == "x16" or reg == "a6":
        bin_code = "10000"
    elif reg == "x17" or reg == "a7":
        bin_code = "10001"
    elif reg == "x18" or reg == "s2":
        bin_code = "10010"
    elif reg == "x19" or reg == "s3":
        bin_code = "10011"
    elif reg == "x20" or reg == "s4":
        bin_code = "10100"
    elif reg == "x21" or reg == "s5":
        bin_code = "10101"
    elif reg == "x22" or reg == "s6":
        bin_code = "10110"
    elif reg == "x23" or reg == "s7":
        bin_code = "10111"
    elif reg == "x24" or reg == "s8":
        bin_code = "11000"
    elif reg == "x25" or reg == "s9":
        bin_code = "11001"
    elif reg == "x26" or reg == "s10":
        bin_code = "11010"
    elif reg == "x27" or reg == "s11":
        bin_code = "11011"
    elif reg == "x28" or reg == "t3":
        bin_code = "11100"
    elif reg == "x29" or reg == "t4":
        bin_code = "11101"
    elif reg == "x30" or reg == "t5":
        bin_code = "11110"
    elif reg == "x31" or reg == "t6":
        bin_code = "11111"
    return bin_code

@app.route('/', methods = ['get'])
def Homepage():
    session['stateofasm'] = 0 # There's no PC values at the beginning of each line, 1 for PC values

    return render_template("Homepage.html")
@app.route('/assemble', methods = ['post'])
def assemble():
    asm = request.form["asm"]
    all = list(asm.split('\r\n'))
    linenumber = 0
    Label = []
    Labelposition = []
    Instruction = []
    lines = []
    try:
        for line in all:
            if len(line.strip()) == 0 or line.strip().startswith("#") or line.strip().startswith("//"):
                continue
            if line.find('#') != -1:
                line = line[:line.find('#')].strip()
            if line.find('//') != -1:
                line = line[:line.find('//')].strip()
            if line.find(':') == -1:
                # print(len(line), line)
                lines.append(line)
                linenumber += 1
            else:
                if line not in Label:
                    Label.append(line[:line.find(':')])
                    Labelposition.append(linenumber)
                else:
                    WrongAssemble = "Label at line {} of {} has existed more than once!".format(linenumber, line)
                    return render_template("Homepage.html", WrongAssemble = WrongAssemble)
        linenumber = 0
        errInfo = ""
        for line in lines:
            binary = ""
            op = line.split()[0]
            # R type
            if op.lower() in inst_R.keys():
                regs = line[line.find(line.split()[1]):].split(',')
                if len(regs) != 3:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(3, len(regs), line)
                    break
                rd  = Reg_to_Bin(regs[0].strip())
                rs1 = Reg_to_Bin(regs[1].strip())
                rs2 = Reg_to_Bin(regs[2].strip())
                if rd == "$$" or rs1 == "$$" or rs2 == "$$":
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                binary = inst_R[op.lower()][2] + rs2 + rs1 + inst_R[op.lower()][1] + rd + "0110011"
            # I type
            elif op.lower() in inst_I.keys():
                paras = line[line.find(line.split()[1]):].split(',')
                if len(paras) != 3:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(3, len(paras), line)
                    break
                rd = Reg_to_Bin(paras[0].strip())
                rs1 = Reg_to_Bin(paras[1].strip())
                imm = paras[2].strip()
                if rd == "$$" or rs1 == "$$" or is_imm(imm) == False:
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                if op.lower() in {"slli", "srli", "srai"}:
                    if eval(imm) < 0 or eval(imm) > 31:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    binary = inst_I[op.lower()][2] + bin(eval(imm))[2:].rjust(5, '0') + \
                             rs1 + inst_I[op.lower()][1] + rd + "0010011"
                else:
                    if eval(imm) < -2048 or eval(imm) > 2047:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    binary += bin2comp(eval(imm))
                    binary += rs1 + inst_I[op.lower()] + rd + "0010011"
            # Load and Store
            elif op.lower() in inst_L.keys() or op.lower() in inst_S.keys():
                paras = line[line.find(line.split()[1]):].split(',')
                if len(paras) != 2:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(2, len(paras), line)
                    break
                rd = Reg_to_Bin(paras[0].strip())
                if rd == "$$":
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                num_reg = paras[1].strip()
                offset = 0
                if num_reg.find('(') != 0:
                    offset = eval(num_reg[:num_reg.find('(')])
                    if offset < -2048 or offset > 2047:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                rs1 = Reg_to_Bin(num_reg[num_reg.find('(') + 1 : num_reg.find(')')])
                if rs1 == "$$":
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                if op.lower() in inst_L.keys():
                    binary = bin2comp(offset) + rs1 + inst_L[op.lower()] + rd + "0000011"
                else:
                    binary = bin2comp(offset)[:7] + rd + rs1 + inst_S[op.lower()] + bin2comp(offset)[7:] + "0100011"
            elif op.lower() in inst_B:
                paras = line[line.find(line.split()[1]):].split(',')
                if len(paras) != 3:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(3, len(paras), line)
                    break
                rs1 = Reg_to_Bin(paras[0].strip())
                rs2 = Reg_to_Bin(paras[1].strip())
                if rs1 == "$$" or rs2 == "$$":
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                imm = str(paras[2].strip())
                if is_imm(imm):
                    imm = eval(imm)
                    if imm < -4096 or imm > 4095:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    imm = bin2comp(imm)
                else: # label
                    if imm not in Label:
                        errInfo = "Error at line {}: the label {} has not existed!".format(linenumber, imm)
                        break
                    imm = Labelposition[Label.index(imm)]
                    imm = imm - linenumber # no - 1, PC is used here instead of PC + 4
                    if imm < -4096 or imm > 4095:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    imm = bin2comp(imm * 2)
                binary = imm[0] + imm[2:8] + rs2 + rs1 + inst_B[op.lower()] + imm[8:12] + imm[1] + "1100011"
            elif op.lower() == "jal":
                paras = line[line.find(line.split()[1]):].split(',')
                if len(paras) != 2:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(2, len(paras), line)
                    break
                rd = Reg_to_Bin(paras[0].strip())
                if rd == "$$":
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                imm = str(paras[1].strip())
                if is_imm(imm):
                    imm = eval(imm)
                    if imm < -1048576 or imm > 1048575:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    imm = bin2comp20(imm // 2)
                else: # label
                    if imm not in Label:
                        errInfo = "Error at line {}: the label {} has not existed!".format(linenumber, imm)
                        break
                    # print("Labelposition: ", Labelposition[Label.index(imm)])
                    # print("linenumber:", linenumber)
                    imm = Labelposition[Label.index(imm)]
                    imm = imm - linenumber # 4-byte offset
                    if imm < -1048576 or imm > 1048575:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    imm = bin2comp20(imm * 2)
                binary = imm[0] + imm[10:20] + imm[9] + imm[1:9] + rd + "1101111"
            elif op.lower() == "jalr":
                paras = line[line.find(line.split()[1]):].split(',')
                if len(paras) != 3:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(3, len(paras), line)
                    break
                rd = Reg_to_Bin(paras[0].strip())
                rs1 = Reg_to_Bin(paras[1].strip())
                if rd == "$$" or rs1 == "$$":
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                imm = str(paras[2].strip())
                if is_imm(imm):
                    imm = eval(imm)
                    if imm < -4096 or imm > 4095:
                        errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                        break
                    imm = bin2comp(imm)
                else: # label
                    errInfo = "Line {}: {}; jalr can only handle imm, no label allowed!".format(linenumber, line)
                    break
                binary = imm + rs1 + "000" + rd + "1100111"
            elif op.lower() == "lui" or op.lower() == "auipc":
                paras = line[line.find(line.split()[1]):].split(',')
                if len(paras) != 2:
                    errInfo = "Expected {} parameters, got {}, inst: {}".format(2, len(paras), line)
                    break
                rd = Reg_to_Bin(paras[0].strip())
                imm = paras[1].strip()
                if rd == "$$" or is_imm(imm) == False:
                    errInfo = "Wrong parameter in line {}: {}".format(linenumber, line)
                    break
                if eval(imm) < 0 or eval(imm) > 1048575: # unsigned
                    errInfo = "imm out of range in line {}: {}".format(linenumber, line)
                    break
                binary = bin2comp20(eval(imm)) + rd
                if op.lower() == "lui":
                    binary += "0110111"
                else:
                    binary += "0010111"
            else:
                errInfo = "Unrecognized / Unsupported Opcode!"
                return render_template("Homepage.html", WrongAssemble = errInfo)
            Instruction.append(binary)
            linenumber += 1
            


            
        if len(errInfo) != 0:
            return render_template("Homepage.html", WrongAssemble = errInfo)
        # to coe format
        '''
        result = "memory_initialization_radix=16;\r\nmemory_initialization_vector=\r\n"
        i = 0
        while i < len(Instruction) - 1:
            tempbin = int(Instruction[i], base = 2)
            temphex = hex(tempbin)[2:] # to a hex string
            temphex = temphex.rjust(8, '0')
            result += temphex
            result += ',\r\n'
            i += 1
        tempbin = int(Instruction[i], base = 2)
        temphex = hex(tempbin)[2:] # to a hex string
        temphex = temphex.rjust(8, '0')
        result += temphex
        result += ';'
        '''
        # to hex format (for $readmemh)
        result = ""
        i = 0
        while i < len(Instruction) - 1:
            tempbin = int(Instruction[i], base = 2)
            temphex = hex(tempbin)[2:] # to a hex string
            temphex = temphex.rjust(8, '0')
            result += temphex
            result += '\r\n'
            i += 1
        tempbin = int(Instruction[i], base = 2)
        temphex = hex(tempbin)[2:] # to a hex string
        temphex = temphex.rjust(8, '0')
        result += temphex

        return render_template("Homepage.html", Assembled = result, Disassembled = asm) # Instruction
    except Exception as e:
        return render_template("Homepage.html", WrongAssemble = e)


@app.route('/disassemble', methods = ['post'])
def disassemble():
    hex = request.form["hex"]
    temp = []
    lines = []
    # for i in hex:
    #     if i != '\r' and i != '\n':
    #         temp.append(i)
    #     elif i == '\r':
    #         a = "".join(temp).strip()
    #         if a != "":
    #             lines.append("".join(temp).strip())
    #         temp = []
    # a = "".join(temp).strip()
    print(hex)
    try:
        return render_template("Homepage.html")
    except Exception as e:
        return render_template("Homepage.html", WrongDisassemble = e)