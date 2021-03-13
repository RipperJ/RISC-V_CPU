# RISC-V 32i CPU and Assembler

This is one of the course project materials for HKUST ELEC-5140 **Advanced Computer Architecture**, where students are encouraged to enhance the structural model and improve its performance. This project is alive, maintained by [linfeng.du@connect.ust.hk](linfeng.du@connect.ust.hk). Any discussion or suggestion would be greatly appreciated! 

***

## Project Tree

1. **RV32i** directory contains a Vivado project of RISC-V CPU written in verilog, which implements a 5-stage single-issue processor, supporting 31 basic instructions from [RV32I base instruction set](https://riscv.org/wp-content/uploads/2019/12/riscv-spec-20191213.pdf#page=148).

2. **RISC-V_Assembler** directory contains an assembler to translate RISC-V instruction assembly into hexadecimal format, which could be easily directly loaded to instruction memory through `$readmemh` during Vivado simulation.

3. **tests** directory contains benchmark written in RV32i assembly. Vec_Mul is a basic coding example.

***

## Assembly Manual
### What this assembler supports:
* R-type:
```
add s1, t1, t2 # s1 = t1 + t2
```
* I-type:
```
slti s1, t1, 3 # if t1 < 3: s1 = 1; else: s1 = 0;
```
* Load / Store:
```
lw s1, 4(t1) # s1 = *(t1 + 1) // 4 means 4 bytes == 1 word (int size)
sw s1, 4(t1)
```
* Branch:
```
# Using immediate value for address is OK
beq t1, t2, 0x1000
# A more convenient way is using labels, like:

This_Is_A_Label:
# ... 
# ... do whatever you want
# ...
beq t1, t2, This_Is_A_Label // if t1 == t2, then jump to the first instruction after label "This_Is_A_Label"
```
* LUI / AUIPC:
```
lui x2, 0x12345     # x2 = 0x12345000
addi x2, x2, 0x678  # x2 = 0x12345678
auipc x3, 0x0100    # x3 = 0x00100000 + PC
```
* JAL / JALR:
```
jal x1, SOME_LABEL # or some immediate value as address
jalr x0, x1, 0 # only immediate value is allowed for the third parameter!
```
* comments:
```
# This is a line of comment
// This is also a line of comment
add s1, s2, s3 # This is a line of comment following one instruction
add s1, s2, s3 // This is also a line of comment following one instruction
```
* Others
```
# 1. Case Insensitivity
add s1, t1, t2 // OK
ADD s2, t1, t1 // also OK
# 2. Supporting both Register Name and ABI Name
// Instead of using register name 'x0', 'x1', you can also use 'zero', 'ra',
// which makes your assembly more readable
```

***

## TODO
* Assembler
    * [Pseudo Ops](https://github.com/riscv/riscv-asm-manual/blob/master/riscv-asm.md#pseudo-ops)
    * [Pseudo Instructions](https://riscv.org/wp-content/uploads/2019/12/riscv-spec-20191213.pdf#page=157)
    * Make it good-looking...

* CPU
    * To support other basic instructions
        * LB, LH, LBU, LHU
        * SB, SH
        * FENCE, FENCE.I
        * ECALL, EBREAK
        * CSRR*

***

## Reference Link for students
1. [The RISC-V Instruction Set Manual](https://riscv.org/wp-content/uploads/2019/12/riscv-spec-20191213.pdf)
    * [RV32i Registers](https://riscv.org/wp-content/uploads/2019/12/riscv-spec-20191213.pdf#page=155): only x0 ~ x31 are used here.
    * [RV32I base instruction set](https://riscv.org/wp-content/uploads/2019/12/riscv-spec-20191213.pdf#page=148)