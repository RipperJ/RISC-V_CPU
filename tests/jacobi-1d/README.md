This includes test of "jal" and "jalr".

You can assemble the "main.asm" on Assembler webpage yourself, or directly use the "./main.hex".
The "./main.c" program is a X86 C program, you can compile it with gcc. The "a.out" is the corresponding executable file.
Please copy the content of "./main.hex" to "[base dir]/RV32i/RV32i.sim/sim_1/behav/xsim/ROM_data.txt" and run simulation to test the effect.

* As the "Vec_Mul" program, the final step is to save a number 1 at the first line of data RAM (address 0x00000000), which would trigger the "$stop" condition in the same simulation file.
* In the screenshot (png file), "Data_RAM[128:137]" corresponds with array "A", and "Data_RAM[192:201]" corresponds with array "B".
