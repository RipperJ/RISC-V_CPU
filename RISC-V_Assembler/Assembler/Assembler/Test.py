
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, request
from Assembler import app
# The function return the binary number of a register
def rev(string):
    string = list(string)
    i = 0
    while i < len(string):
        if string[i] == '0':
            string[i] = '1'
        else:
            string[i] = '0'
        i += 1
    value = int("".join(string), base = 2) + 1
    binary = bin(value)
    binary = binary[2:].rjust(len(string), '1')[-len(string):]
    return binary
def rev1(string):
    string = list(string)
    i = 0
    while i < len(string):
        if string[i] == '0':
            string[i] = '1'
        else:
            string[i] = '0'
        i += 1
    value = int("".join(string), base = 2) + 1
    binary = bin(value)
    binary = binary[2:].rjust(len(string), '0')[-len(string):]
    return binary
def extendbynum(string, num):
    if num == 0:
        string += '$zero'
    elif num == 1:
        string += '$at'
    elif num == 2:
        string += '$v0'
    elif num == 3:
        string += '$v1'
    elif num == 4:
        string += '$a0'
    elif num == 5:
        string += '$a1'
    elif num == 6:
        string += '$a2'
    elif num == 7:
        string += '$a3'
    elif num == 8:
        string += '$t0'
    elif num == 9:
        string += '$t1'
    elif num == 10:
        string += '$t2'
    elif num == 11:
        string += '$t3'
    elif num == 12:
        string += '$t4'
    elif num == 13:
        string += '$t5'
    elif num == 14:
        string += '$t6'
    elif num == 15:
        string += '$t7'
    elif num == 16:
        string += '$s0'
    elif num == 17:
        string += '$s1'
    elif num == 18:
        string += '$s2'
    elif num == 19:
        string += '$s3'
    elif num == 20:
        string += '$s4'
    elif num == 21:
        string += '$s5'
    elif num == 22:
        string += '$s6'
    elif num == 23:
        string += '$s7'
    elif num == 24:
        string += '$t8'
    elif num == 25:
        string += '$t9'
    elif num == 28:
        string += '$gp'
    elif num == 29:
        string += '$sp'
    elif num == 30:
        string += '$fp'
    elif num == 31:
        string += '$ra'
    return string

def extendbyreg(string, reg):
    if reg.lower() == '$zero':
        string += '00000'
    elif reg.lower() == '$at':
        string += '00001'
    elif reg.lower() == '$v0':
        string += '00010'
    elif reg.lower() == '$v1':
        string += '00011'
    elif reg.lower() == '$a0':
        string += '00100'
    elif reg.lower() == '$a1':
        string += '00101'
    elif reg.lower() == '$a2':
        string += '00110'
    elif reg.lower() == '$a3':
        string += '00111'
    elif reg.lower() == '$t0':
        string += '01000'
    elif reg.lower() == '$t1':
        string += '01001'
    elif reg.lower() == '$t2':
        string += '01010'
    elif reg.lower() == '$t3':
        string += '01011'
    elif reg.lower() == '$t4':
        string += '01100'
    elif reg.lower() == '$t5':
        string += '01101'
    elif reg.lower() == '$t6':
        string += '01110'
    elif reg.lower() == '$t7':
        string += '01111'
    elif reg.lower() == '$s0':
        string += '10000'
    elif reg.lower() == '$s1':
        string += '10001'
    elif reg.lower() == '$s2':
        string += '10010'
    elif reg.lower() == '$s3':
        string += '10011'
    elif reg.lower() == '$s4':
        string += '10100'
    elif reg.lower() == '$s5':
        string += '10101'
    elif reg.lower() == '$s6':
        string += '10110'
    elif reg.lower() == '$s7':
        string += '10111'
    elif reg.lower() == '$t8':
        string += '11000'
    elif reg.lower() == '$t9':
        string += '11001'
    elif reg.lower() == '$gp':
        string += '11100'
    elif reg.lower() == '$sp':
        string += '11101'
    elif reg.lower() == '$fp':
        string += '11110'
    elif reg.lower() == '$ra':
        string += '11111'
    return string


@app.route('/', methods = ['get'])
def Homepage():
    session['stateofasm'] = 0 # There's no PC values at the beginning of each line, 1 for PC values

    return render_template("Homepage.html")

@app.route('/assemble', methods = ['post'])
def assemble():
    asm = request.form['asm'] # get the assembly
    # Transform to instructions first
    lines = []
    temp = []
    position = 0
    for i in asm:
        if i != '\r' and i != '\n':
            temp.append(i)
        elif i == '\r':
            a = "".join(temp).strip()
            if a != "":
                lines.append("".join(temp).strip())
            temp = []
    a = "".join(temp).strip()
    if a != "":
        lines.append("".join(temp).strip()) # Each line is saved in variable 'lines'
    #print(lines)
    initialline = 0 # record the start address
    linenumber = 0
    Label = []
    Labelposition = []
    Instruction = []
    Instructionposition = []
    # The empty lines have already been removed
    try:
        for i in lines:
            # A whole line of comment: jump over directly
            if i.strip().find('#') == 0 or i.strip().find('//') == 0:
                continue
            if i.find('#') != -1:
                i = i[:i.find('#')].strip()
            elif i.find('//') != -1:
                i = i[:i.find('//')].strip()
            # All comments have been removed
            if i.find(':') == -1: # only instructions has got comma in it hahaha, emm but not all instructions have ',' like "j"
                linenumber += 1
            else: # for labels
                if i not in Label:
                    Label.append(i[:i.find(':')])
                    Labelposition.append(linenumber)
                else: # overlapping labels: error
                    WrongAssemble = "Label at line {} of {} has existed more than once!".format(linenumber, i)
                    return render_template("Homepage.html", WrongAssemble = WrongAssemble)
        #print(Label, Labelposition) # Symbol Table has been created
        linenumber = 0
        for i in lines:
            # A whole line of comment: jump over directly
            if i.strip().find('#') == 0 or i.strip().find('//') == 0:
                continue
            if i.find('#') != -1:
                i = i[:i.find('#')].strip().strip(';')
            elif i.find('//') != -1:
                i = i[:i.find('//')].strip().strip(';')
            # All comments have been removed
            #print(i)
            if i.find(':') == -1: # This is an instruction, labels are omitted
                #i = i[:i.find(';')] # The ; at the end is removed, this old way has been abandoned
                binary = ""
                op = i.split()[0]
                if op.lower() == 'add':
                    binary += "000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    #print(reg3)
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[2].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    binary += '00000100000'
                elif op.lower() == 'sub':
                    binary += "000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[2].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    binary += '00000100010'
                elif op.lower() == 'and':
                    binary += "000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[2].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    binary += '00000100100'
                elif op.lower() == 'or':
                    binary += "000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[2].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    binary += '00000100101'
                elif op.lower() == 'addi':
                    binary += "001000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[0].strip()
                    binary = extendbyreg(binary, rt)
                    imm = eval(reg3[2].strip())
                    if imm > 65535 or imm < -32768:
                        WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    if imm < 0:
                        imm = bin(imm)[3:]
                        imm = imm.rjust(16, '0') # Fill 1s at the left of the number
                        imm = rev(imm)
                    elif imm > 32767:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0') # Fill 1s at the left of the number
                        imm = rev(imm)
                    else:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0') # Fill 0s at the left of the number
                    binary += imm
                elif op.lower() == 'ori':
                    binary += "001101"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[0].strip()
                    binary = extendbyreg(binary, rt)
                    imm = eval(reg3[2].strip())
                    if imm > 65535 or imm < -32768:
                        WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    if imm < 0:
                        imm = bin(imm)[3:]
                        imm = imm.rjust(16, '0') # Fill 1s at the left of the number
                        imm = rev(imm)
                    elif imm > 32767:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0') # Fill 1s at the left of the number
                        imm = rev(imm)
                    else:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0') # Fill 0s at the left of the number
                    binary += imm
                elif op.lower() == 'sll':
                    binary += "00000000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rt = reg3[1].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    shamt = eval(reg3[2].strip())
                    if shamt > 31 or shamt < 0:
                        WrongAssemble = "The shamt at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    shamt = bin(shamt)[2:]
                    shamt = shamt.rjust(5, '0')
                    binary += shamt
                    binary += '000000'
                elif op.lower() == 'srl':
                    binary += "00000000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rt = reg3[1].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    shamt = eval(reg3[2].strip())
                    if shamt > 31 or shamt < 0:
                        WrongAssemble = "The shamt at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    shamt = bin(shamt)[2:]
                    shamt = shamt.rjust(5, '0')
                    binary += shamt
                    binary += '000010'
                elif op.lower() == 'lw':
                    binary += "100011"
                    reg2 = i[i.find(i.split()[1]):].split(',')
                    rt = reg2[0].strip()
                    num_reg = reg2[1].strip()
                    if num_reg.find('(') == 0:
                        offset = 0
                    else:
                        offset = eval(num_reg[:num_reg.find('(')])
                    rs = num_reg[num_reg.find('(') + 1:num_reg.find(')')].strip()
                    binary = extendbyreg(binary, rs)
                    binary = extendbyreg(binary, rt)
                    if offset > 65535 or offset < -32768:
                        WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    if offset < 0:
                        offset = bin(offset)[3:]
                        offset = offset.rjust(16, '0') # Fill 1s at the left of the number
                        offset = rev(offset)
                    elif offset > 32767:
                        offset = bin(offset)[2:]
                        offset = offset.rjust(16, '0') # Fill 1s at the left of the number
                        offset = rev(offset)
                    else:
                        offset = bin(offset)[2:]
                        offset = offset.rjust(16, '0') # Fill 0s at the left of the number
                    binary += offset
                elif op.lower() == 'sw':
                    binary += "101011"
                    reg2 = i[i.find(i.split()[1]):].split(',')
                    rt = reg2[0].strip()
                    num_reg = reg2[1].strip()
                    if num_reg.find('(') == 0:
                        offset = 0
                    else:
                        offset = eval(num_reg[:num_reg.find('(')])
                    rs = num_reg[num_reg.find('(') + 1:num_reg.find(')')].strip()
                    binary = extendbyreg(binary, rs)
                    binary = extendbyreg(binary, rt)
                    if offset > 65535 or offset < -32768:
                        WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    if offset < 0:
                        offset = bin(offset)[3:]
                        offset = offset.rjust(16, '0') # Fill 1s at the left of the number
                        offset = rev(offset)
                    elif offset > 32767:
                        offset = bin(offset)[2:]
                        offset = offset.rjust(16, '0') # Fill 1s at the left of the number
                        offset = rev(offset)
                    else:
                        offset = bin(offset)[2:]
                        offset = offset.rjust(16, '0') # Fill 0s at the left of the number
                    binary += offset
                elif op.lower() == 'lui':
                    binary += "00111100000"
                    reg2 = i[i.find(i.split()[1]):].split(',')
                    rt = reg2[0].strip()
                    imm = eval(reg2[1].strip())
                    binary = extendbyreg(binary, rt)
                    if imm > 65535 or imm < -32768:
                        WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    if imm < 0:
                        imm = bin(imm)[3:]
                        imm = imm.rjust(16, '0')
                        imm = rev(imm)
                    elif imm > 32767:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0')
                        imm = rev(imm)
                    else:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0')
                    binary += imm
                elif op.lower() == 'slt':
                    binary += "000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[2].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    binary += '00000101010'
                elif op.lower() == 'slti':
                    binary = "001010"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[0].strip()
                    binary = extendbyreg(binary, rt)
                    imm = eval(reg3[2].strip())
                    if imm > 65535 or imm < -32768:
                        WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                    if imm < 0:
                        imm = bin(imm)[3:]
                        imm = imm.rjust(16, '0')
                        imm = rev(imm)
                    elif imm > 32767:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0')
                        imm = rev(imm)
                    else:
                        imm = bin(imm)[2:]
                        imm = imm.rjust(16, '0')
                    binary += imm
                elif op.lower() == 'beq':
                    binary = "000100"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[0].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[1].strip()
                    binary = extendbyreg(binary, rt)
                    # Label or num
                    imm = reg3[2].strip()
                    if imm.isdigit() or (imm[1:].isdigit() and imm[0] == '-'): # an immediate number
                        imm = eval(imm)
                        if imm > 65535 or imm < -32768:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        if imm < 0:
                            imm = bin(imm)[3:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        elif imm > 32767:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        else:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                    elif imm[0:2] == '0x' or imm[0:3] == '-0x':
                        imm = eval(imm) # from hex to dec
                        if imm > 65535 or imm < -32768:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        if imm < 0:
                            imm = bin(imm)[3:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        elif imm > 32767:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        else:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                    else: # a label
                        if imm not in Label:
                            WrongAssemble = "Error at line {}: the label {} has not existed!".format(linenumber, imm)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        else:
                            imm = Labelposition[Label.index(imm)]
                            imm = imm - linenumber - 1
                            if imm > 32767 or imm < -32768:
                                WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                                return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                            if imm < 0:
                                imm = bin(imm)[3:]
                                imm = imm.rjust(16, '0')
                                imm = rev(imm)
                            else:
                                imm = bin(imm)[2:]
                                imm = imm.rjust(16, '0')
                    binary += imm
                elif op.lower() == 'bne':
                    binary = "000101"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[0].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[1].strip()
                    binary = extendbyreg(binary, rt)
                    # Label or num
                    imm = reg3[2].strip()
                    if imm.isdigit() or (imm[1:].isdigit() and imm[0] == '-'): # an immediate number
                        imm = eval(imm)
                        if imm > 65535 or imm < -32768:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        if imm < 0:
                            imm = bin(imm)[3:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        elif imm > 32767:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        else:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                    elif imm[0:2] == '0x' or imm[0:3] == '-0x':
                        imm = eval(imm) # from hex to dec
                        if imm > 65535 or imm < -32768:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        if imm < 0:
                            imm = bin(imm)[3:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        elif imm > 32767:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                            imm = rev(imm)
                        else:
                            imm = bin(imm)[2:]
                            imm = imm.rjust(16, '0')
                    else: # a label
                        if imm not in Label:
                            WrongAssemble = "Error at line {}: the label {} has not existed!".format(linenumber, imm)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        else:
                            imm = Labelposition[Label.index(imm)]
                            imm = imm - linenumber - 1
                            if imm > 32767 or imm < -32768:
                                WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                                return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                            if imm < 0:
                                imm = bin(imm)[3:]
                                imm = imm.rjust(16, '0')
                                imm = rev(imm)
                            else:
                                imm = bin(imm)[2:]
                                imm = imm.rjust(16, '0')
                    binary += imm
                    #print(binary)
                elif op.lower() == 'j': # 26-bit target !!!!!!!!!!!!!!!!!!!!!
                    binary = "000010"
                    target = i[i.find(i.split()[1]):].strip()
                    if target.isdigit() or (target[1:].isdigit() and target[0] == '-'): # an immediate number
                        target = eval(target) # address = immediate
                        if target > 67108863 or target < 0:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        target = bin(target)[2:]
                        target = target.rjust(26, '0')
                    elif target[0:2] == '0x' or target[0:3] == '-0x':
                        target = eval(target) # from hex to dec, address = immediate
                        if target > 67108863 or target < 0:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        target = bin(target)[2:]
                        target = target.rjust(26, '0')
                    else: # a label
                        if target not in Label:
                            WrongAssemble = "Error at line {}: the label {} has not existed!".format(linenumber, target)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        else:
                            target = Labelposition[Label.index(target)]
                            #target = target - linenumber - 1
                            if target > 67108863 or target < 0:
                                WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                                return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                            target = bin(target)[2:]
                            target = target.rjust(26, '0')
                    binary += target
                elif op.lower() == 'jal':
                    binary = "000011"
                    target = i[i.find(i.split()[1]):].strip()
                    if target.isdigit() or (target[1:].isdigit() and target[0] == '-'): # an immediate number
                        target = eval(target) # address = immediate
                        if target > 67108863 or target < 0:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        target = bin(target)[2:]
                        target = target.rjust(26, '0')
                    elif target[0:2] == '0x' or target[0:3] == '-0x':
                        target = eval(target) # from hex to dec, address = immediate
                        if target > 67108863 or target < 0:
                            WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        target = bin(target)[2:]
                        target = target.rjust(26, '0')
                    else: # a label
                        if target not in Label:
                            WrongAssemble = "Error at line {}: the label {} has not existed!".format(linenumber, target)
                            return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                        else:
                            target = Labelposition[Label.index(target)]
                            #target = target - linenumber - 1
                            if target > 67108863 or target < 0:
                                WrongAssemble = "The immediate at line = {} is out of range!".format(linenumber)
                                return render_template("Homepage.html", WrongAssemble = WrongAssemble)
                            target = bin(target)[2:]
                            target = target.rjust(26, '0')
                    binary += target
                elif op.lower() == 'jr':
                    binary = "000000"
                    reg1 = i[i.find(i.split()[1]):].strip()
                    binary = extendbyreg(binary, reg1)
                    binary += "000000000000000001000"
                elif op.lower() == 'nor':
                    binary += "000000"
                    reg3 = i[i.find(i.split()[1]):].split(',')
                    rs = reg3[1].strip()
                    binary = extendbyreg(binary, rs)
                    rt = reg3[2].strip()
                    binary = extendbyreg(binary, rt)
                    rd = reg3[0].strip()
                    binary = extendbyreg(binary, rd)
                    binary += '00000100111'
                Instruction.append(binary) # !!!!!!!!!!!16
                Instructionposition.append(linenumber)
                linenumber += 1
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
        #print(Label)
        #print(Labelposition)
        return render_template("Homepage.html", Assembled = result)
    except Exception as E:
        WrongAssemble = "Error at line {}: ".format(linenumber) + str(E)
        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
    return render_template("Homepage.html")

@app.route('/disassemble', methods = ['post'])
def disassemble():
    HEX = request.form['hex'] # get the assembly
    # Transform to instructions first
    initialline = 0 # record the start address
    lines = ""
    temp = []
    position = 0
    for i in HEX:
        if i != '\r' and i != '\n':
            temp.append(i)
        elif i == '\r':
            a = "".join(temp).strip()
            if a != "":
                lines += a
            temp = []
    a = "".join(temp).strip()
    if a != "":
        lines += a # Each line is saved in variable 'lines'
    #print(lines)
    if lines == "":
        return render_template("Homepage.html")
    try:
        lines = lines.strip("memory_initialization_radix").strip().strip('=').strip().strip('16').strip().strip(';')
        lines = lines[28:].strip().strip('=')
        #print(lines) # now, only the instructions are left
        Instructions = lines.split(',')
        Totalines = len(Instructions) # The total number of instructions
        #print(Totalines)
        Initial = 0 # the start of MIPS code
        Insts = []
        Label = []
        Labelposition = []
        Labelnumber = 0
        #print(Instructions)
        for i in Instructions:
            Inst = ""
            Instruction = i.strip() # pure instruction
            binary = bin(int(Instruction, base = 16))[2:].rjust(32, '0') # 32-bit binary string
            #print(binary)
            if binary[0:6] == '000000': # all r-type are here
                if binary[-6:] == '100000': # 1. add
                    Inst = "add\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ';'
                elif binary[-6:] == '100010': # 2. sub
                    Inst = "sub\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ';'
                elif binary[-6:] == '100100': # 3. and
                    Inst = "and\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ';'
                elif binary[-6:] == '100101': # 4. or
                    Inst = "or\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ';'
                elif binary[-6:] == '000000' and binary[6:11] == '00000': # 5. sll
                    Inst = "sll\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ', '
                    shamt = str(int(binary[21:26], base = 2))
                    Inst += shamt
                    Inst += ';'
                elif binary[-6:] == '000010' and binary[6:11] == '00000': # 6. srl
                    Inst = "srl\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ', '
                    shamt = str(int(binary[21:26], base = 2))
                    Inst += shamt
                    Inst += ';'
                elif binary[-6:] == '101010': # 7. slt
                    Inst = "slt\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ';'
                elif binary[-6:] == '100111': # 8. nor
                    Inst = "nor\t"
                    rd = int(binary[16:21], base = 2)
                    Inst = extendbynum(Inst, rd)
                    Inst += ', '
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ', '
                    rt = int(binary[11:16], base = 2)
                    Inst = extendbynum(Inst, rt)
                    Inst += ';'
                elif binary[-6:] == '001000': # 9. jr
                    Inst = "jr\t"
                    rs = int(binary[6:11], base = 2)
                    Inst = extendbynum(Inst, rs)
                    Inst += ';'
            elif binary[0:6] == '001000': # 10. addi
                Inst = "addi\t"
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate value
                    imm = rev1(binary[16:])
                    flag = 1
                else: # a positive immediate
                    imm = binary[16:]
                imm = int(imm, base = 2)
                if flag == 1:
                    Inst += '-'
                Inst += str(imm) + ';'
            elif binary[0:6] == '001101': # 11. ori
                Inst = "ori\t"
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate value
                    imm = rev1(binary[16:])
                    flag = 1
                else: # a positive immediate
                    imm = binary[16:]
                imm = int(imm, base = 2)
                if flag == 1:
                    Inst += '-'
                Inst += str(imm) + ';'
            elif binary[0:6] == '100011': # 12. lw
                Inst = "lw\t"
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate value
                    imm = rev1(binary[16:])
                    flag = 1
                else: # a positive immediate
                    imm = binary[16:]
                imm = int(imm, base = 2)
                if flag == 1:
                    Inst += '-'
                Inst += str(imm) + '('
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ');'
            elif binary[0:6] == '101011': # 13. sw
                Inst = "sw\t"
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate value
                    imm = rev1(binary[16:])
                    flag = 1
                else: # a positive immediate
                    imm = binary[16:]
                imm = int(imm, base = 2)
                if flag == 1:
                    Inst += '-'
                Inst += str(imm) + '('
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ');'
            elif binary[0:6] == '001111': # 14. lui
                Inst = "lui\t"
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate value
                    imm = rev1(binary[16:])
                    flag = 1
                else: # a positive immediate
                    imm = binary[16:]
                imm = int(imm, base = 2)
                if flag == 1:
                    Inst += '-'
                Inst += str(imm) + ';'
            elif binary[0:6] == '001010': # 15. slti
                Inst = "slti\t"
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate value
                    imm = rev1(binary[16:])
                    flag = 1
                else: # a positive immediate
                    imm = binary[16:]
                imm = int(imm, base = 2)
                if flag == 1:
                    Inst += '-'
                Inst += str(imm) + ';'
            elif binary[0:6] == '000100': # 16. beq
                Inst = "beq\t"
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ', '
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate
                    imm = rev1(binary[16:])
                    flag = 1
                else:
                    imm = binary[16:]
                imm = int(imm, base = 2)
                # Then check whether it jumps out of the code range
                current_position = len(Insts) + 1 # the number of instruction corresponding to PC + 4
                if flag == 1:
                    destination = current_position - imm
                else:
                    destination = current_position + imm
                if destination < initialline or destination > Totalines: # when exceeds the range, use immediate value
                    if flag == 1:
                        Inst += '-'
                    Inst += str(imm) + ';'
                else: # within the code range
                    if Labelposition.count(destination) != 0:
                        Inst += Label[Labelposition.index(destination)] + ';'
                    else:
                        Label.append("L" + str(Labelnumber))
                        Inst += "L" + str(Labelnumber) + ';'
                        Labelposition.append(destination)
                        Labelnumber += 1
            elif binary[0:6] == '000101': # 17. bne
                Inst = "bne\t"
                rs = int(binary[6:11], base = 2)
                Inst = extendbynum(Inst, rs)
                Inst += ', '
                rt = int(binary[11:16], base = 2)
                Inst = extendbynum(Inst, rt)
                Inst += ', '
                flag = 0
                if binary[16] == '1': # this is a negative immediate
                    imm = rev1(binary[16:])
                    flag = 1
                else:
                    imm = binary[16:]
                imm = int(imm, base = 2)
                # Then check whether it jumps out of the code range
                current_position = len(Insts) + 1 # the number of instruction corresponding to PC + 4
                if flag == 1:
                    destination = current_position - imm
                else:
                    destination = current_position + imm
                #print(destination)
                if destination < initialline or destination > Totalines: # when exceeds the range, use immediate value
                    if flag == 1:
                        Inst += '-'
                    Inst += str(imm) + ';'
                else: # within the code range
                    if Labelposition.count(destination) != 0:
                        Inst += Label[Labelposition.index(destination)] + ';'
                    else:
                        Label.append("L" + str(Labelnumber))
                        Inst += "L" + str(Labelnumber) + ';'
                        Labelposition.append(destination)
                        Labelnumber += 1
            elif binary[0:6] == '000010': # 18. j
                Inst = "j\t"
                flag = 0
                if binary[6] == '1': # this is a negative immediate
                    imm = rev1(binary[6:])
                    flag = 1
                else:
                    imm = binary[6:]
                imm = int(imm, base = 2)
                # Then check whether it jumps out of the code range
                #current_position = len(Insts) # the number of instruction corresponding to 
                #print(imm)
                #if flag == 1:
                #    destination = current_position - imm
                #else:
                #    destination = current_position + imm // 4
                destination = imm
                #print(destination)
                if destination < initialline or destination > Totalines: # when exceeds the range, use immediate value
                    if flag == 1:
                        Inst += '-'
                    Inst += str(imm) + ';'
                else: # within the code range
                    if Labelposition.count(destination) != 0:
                        Inst += Label[Labelposition.index(destination)] + ';'
                    else:
                        Label.append("L" + str(Labelnumber))
                        Inst += "L" + str(Labelnumber) + ';'
                        Labelposition.append(destination)
                        Labelnumber += 1
            elif binary[0:6] == '000011': # 19. jal
                Inst = "jal\t"
                flag = 0
                if binary[6] == '1': # this is a negative immediate
                    imm = rev1(binary[6:])
                    flag = 1
                else:
                    imm = binary[6:]
                imm = int(imm, base = 2)
                # Then check whether it jumps out of the code range
                #current_position = len(Insts) + 1 # the number of instruction corresponding to PC + 4
                #if flag == 1:
                #    destination = current_position - imm // 4
                #else:
                #    destination = current_position + imm // 4
                destination = imm
                if destination < initialline or destination > Totalines: # when exceeds the range, use immediate value
                    if flag == 1:
                        Inst += '-'
                    Inst += str(imm) + ';'
                else: # within the code range
                    if Labelposition.count(destination) != 0:
                        Inst += Label[Labelposition.index(destination)] + ';'
                    else:
                        Label.append("L" + str(Labelnumber))
                        Inst += "L" + str(Labelnumber) + ';'
                        Labelposition.append(destination)
                        Labelnumber += 1
            Insts.append(Inst)
        #print(Insts)
        #print(Label)
        #print(Labelposition)
        result = ""
        i = 0
        while i < len(Insts):
            if i in Labelposition:
                result += Label[Labelposition.index(i)] + ":\r\n"
            linenum = hex(i * 4 + initialline)[2:].rjust(8, '0')
            result += Insts[i] + "\t// PC = " + linenum + "\r\n"
            i += 1
        if i in Labelposition:
            result += Label[Labelposition.index(i)] + ":\r\n"
        #print(result)
        return render_template("Homepage.html", Disassembled = result)
    except Exception as E:
        WrongAssemble = "Error at line {}: ".format(binary) + str(E)
        return render_template("Homepage.html", WrongAssemble = WrongAssemble)
    return render_template("Homepage.html")