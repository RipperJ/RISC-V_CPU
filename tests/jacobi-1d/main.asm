main:
addi s0, x0, 10 // int n = N (N==10);
addi s1, x0, 5 // int tsteps = 5;
addi s2, x0, 0x200 // starting addr of array A
addi s3, x0, 0x300 // starting addr of array B

jal ra, init_array

jal ra, kernel

jal ra, continue

// ----------------------------
kernel:
addi t4, s0, -1
addi t0, x0, 0 
k_loop_t:

addi t1, x0, 1
k_loop_i1:
addi t2, t1, -1
slli t2, t2, 2
add t2, t2, s2
lw t3, 0(t2)
add t5, t3, x0
addi t2, t2, 4
lw t3, 0(t2)
add t5, t5, t3
addi t2, t2, 4
lw t3, 0(t2)
add t5, t5, t3

addi t2, t1, 0
slli t2, t2, 2
add t2, t2, s3
sw t5, 0(t2)
addi t1, t1, 1
bne t1, t4, k_loop_i1

addi t1, x0, 1
k_loop_i2:
addi t2, t1, -1
slli t2, t2, 2
add t2, t2, s3
lw t3, 0(t2)
add t5, t3, x0
addi t2, t2, 4
lw t3, 0(t2)
add t5, t5, t3
addi t2, t2, 4
lw t3, 0(t2)
add t5, t5, t3

addi t2, t1, 0
slli t2, t2, 2
add t2, t2, s2
sw t5, 0(t2)
addi t1, t1, 1
bne t1, t4, k_loop_i2

addi t0, t0, 1
bne t0, s1, k_loop_t

jalr x0, ra, 0
// ----------------------------

// ----------------------------
init_array:
addi t0, x0, 0 // t0: i
addi t3, s2, 0 // addr of A
addi t4, s3, 0 // addr of B
init_loop_i:
addi t1, t0, 2 // data for A[i]
sw t1, 0(t3) // A[i] = i + 2
addi t1, t1, 1 // data for B[i]
sw t1, 0(t4) // B[i] = i + 3
addi t3, t3, 4
addi t4, t4, 4
addi t0, t0, 1
bne t0, s0, init_loop_i
jalr x0, ra, 0
// ----------------------------

continue:
// now A[8] == 146744
lw t0, 32(s2) // t0 = A[8]
srli t0, t0, 9 // t0 = 146744 >> 9 = 286 = 0x11e
addi t0, t0, -285
sw t0, 0(x0)
