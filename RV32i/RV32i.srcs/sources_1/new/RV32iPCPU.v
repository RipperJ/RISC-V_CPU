`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 19:39:55
// Design Name: 
// Module Name: RV32iPCPU
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module RV32iPCPU(
    input clk,
    input rst,
    input [31:0] data_in,   // MEM
    input [31:0] inst_in,   // IF, from PC_out
    
    output [31:0] ALU_out,  // From MEM, address out, for fetching data_in
    output [31:0] data_out, // From MEM, to be written into data memory
    output mem_w,           // From MEM, write valid, for store instructions
    output [31:0] PC_out    // From IF
    );
    wire V5;
    wire N0;
    wire [31:0] Imm_32;
    wire [31:0] add_branch_out;
    wire [31:0] add_jal_out;
    wire [31:0] add_jalr_out;

    wire [4:0] Wt_addr;
    wire [31:0] Wt_data;
    wire [31:0] rdata_A;
    wire [31:0] rdata_B;
    wire [31:0] PC_wb;
    wire [31:0] ALU_A;
    wire [31:0] ALU_B;
    assign V5 = 1'b1;
    assign N0 = 1'b0;
    
    
    wire zero;              // ID
    wire [1:0] Branch;      // ID
    wire ALUSrc_A;          // EXE
    wire [1:0] ALUSrc_B;    // EXE
    wire [4:0] ALU_Control; // EXE
    wire RegWrite;          // WB
    wire [1:0] DatatoReg;   // WB
    
    wire [1:0] B_H_W;       // WB // not used yet
    wire sign;              // WB // not used yet
//    wire RegDst; // WB
//    wire Jal; // WB
    
    // IF_ID
    wire [31:0] IF_ID_inst_in;
    wire [31:0] IF_ID_PC;
    wire [31:0] IF_ID_Data_out;
    wire IF_ID_mem_w;
    wire [4:0] IF_ID_written_reg;
    wire [4:0] IF_ID_read_reg1;
    wire [4:0] IF_ID_read_reg2;
    
    // ID_EXE
    wire [31:0] ID_EXE_inst_in;
    wire [31:0] ID_EXE_PC;
    wire [31:0] ID_EXE_ALU_A;
    wire [31:0] ID_EXE_ALU_B;
    wire [4:0] ID_EXE_ALU_Control;
    wire [31:0] ID_EXE_Data_out;
    wire ID_EXE_mem_w;
    wire [1:0] ID_EXE_DatatoReg;
    wire ID_EXE_RegWrite;
    wire [4:0] ID_EXE_written_reg;
    wire [4:0] ID_EXE_read_reg1;
    wire [4:0] ID_EXE_read_reg2;
    
    wire [31:0] ID_EXE_ALU_out;

    // EXE_MEM
    wire [31:0] EXE_MEM_inst_in;
    wire [31:0] EXE_MEM_PC;
    wire [31:0] EXE_MEM_ALU_out;
    wire [31:0] EXE_MEM_Data_out;
    wire EXE_MEM_mem_w;
    wire [1:0] EXE_MEM_DatatoReg;
    wire EXE_MEM_RegWrite;
    wire [4:0] EXE_MEM_written_reg;
    wire [4:0] EXE_MEM_read_reg1;
    wire [4:0] EXE_MEM_read_reg2;
    
    // MEM_WB
    wire [31:0] MEM_WB_inst_in;
    wire [31:0] MEM_WB_PC;
    wire [31:0] MEM_WB_ALU_out;
    wire [31:0] MEM_WB_Data_in;
    wire [1:0] MEM_WB_DatatoReg;
    wire MEM_WB_RegWrite;
   
   // Stall
   wire PC_dstall;
   wire IF_ID_cstall;
   wire IF_ID_dstall;
   wire ID_EXE_dstall;
   
   
   
    Data_Stall _dstall_ (
        .IF_ID_written_reg(IF_ID_written_reg),
        .IF_ID_read_reg1(IF_ID_read_reg1),
        .IF_ID_read_reg2(IF_ID_read_reg2),
        
        .ID_EXE_written_reg(ID_EXE_written_reg),
        .ID_EXE_read_reg1(ID_EXE_read_reg1),
        .ID_EXE_read_reg2(ID_EXE_read_reg2),
        
        .EXE_MEM_written_reg(EXE_MEM_written_reg),
        .EXE_MEM_read_reg1(EXE_MEM_read_reg1),
        .EXE_MEM_read_reg2(EXE_MEM_read_reg2),
        
        .PC_dstall(PC_dstall),
        .IF_ID_dstall(IF_ID_dstall),
        .ID_EXE_dstall(ID_EXE_dstall)
        );
        
    Control_Stall _cstall_ (
        .Branch(Branch[1:0]),
        .IF_ID_cstall(IF_ID_cstall)
        );

    assign ALU_out = EXE_MEM_ALU_out;
    assign data_out = EXE_MEM_Data_out;
    assign mem_w = EXE_MEM_mem_w;
    
    // IF:-------------------------------------------------------------------------------------------
    // Control Signals:
    //   1. Branch - MUX5 : ID
    // References:
    //   1. inst_in - MUX5 : ID
    //   2. rdata_A - MUX5 : ID
    //   3. Imm_32 - ADD_Branch : ID
    // Pass-on:
    //   1. inst_in (combinatorial)
    //   2. PC
    // Out:
    //   1. PC_out: for fetching inst_in
    REG32 _pc_ (
        .CE(V5),
        .clk(clk),
        .D(PC_wb[31:0]),
        .rst(rst),
        .Q(PC_out[31:0]),
        .PC_dstall(PC_dstall)
        );
    add_32  ADD_Branch (
        .a(IF_ID_PC[31:0]),         // use the "PC" from ID stage
        .b(Imm_32[31:0]),           // From ID stage
        .c(add_branch_out[31:0])    // actually this part belongs to IF_ID
        );   
    add_32 ADD_JAL (
        .a(IF_ID_PC),               // MIPS: PC+4, RISC-V: PC!!!
        .b({{11{IF_ID_inst_in[31]}}, IF_ID_inst_in[31], IF_ID_inst_in[19:12], IF_ID_inst_in[20], IF_ID_inst_in[30:21], 1'b0}), 
        .c(add_jal_out[31:0])
        );
    add_32 ADD_JALR (
        .a(rdata_A[31:0]), 
        .b({{20{IF_ID_inst_in[31]}}, IF_ID_inst_in[31:20]}), 
        .c(add_jalr_out[31:0])
        );
    Mux4to1b32  MUX5 (
        .I0(PC_out[31:0] + 32'b0100),   // From IF stage
        .I1(add_branch_out[31:0]),      // Containing "PC" from ID stage
        .I2(add_jal_out[31:0]),         // From ID stage
        .I3(add_jalr_out[31:0]),        // From ID stage
        .s(Branch[1:0]),                // From ID
        .o(PC_wb[31:0])
        );


    REG_IF_ID _if_id_ (
        .clk(clk), .rst(rst), .CE(V5),
        .IF_ID_dstall(IF_ID_dstall), .IF_ID_cstall(IF_ID_cstall),
        // Input
        .inst_in(inst_in),
        .PC(PC_out),
        // Output
        .IF_ID_inst_in(IF_ID_inst_in),
        .IF_ID_PC(IF_ID_PC)
        );

   // ID:-------------------------------------------------------------------------------------------
   // From IF:
   //   1. inst_in
   //   2. PC
   // Control Signals:
   //   1. RegWrite - Regs : WB
   //   2. ALUSrc_A / ALUSrc_B (stops here)
   // References:
   //   None
   // Pass-on:
   //   1. inst_in
       //   Control_signals {
       //   2. ALU_Control
       //   3. DatatoReg
       //   4. mem_w
       //   5. RegWrite
       //   }
   //   6. ALU_A
   //   7. ALU_B
   //   8. Data_out
   //   9. PC
   // Out:
   //   None
   
    Get_rw_regs _rw_regs_ (
        .inst_in(IF_ID_inst_in[31:0]),
        .written_reg(IF_ID_written_reg),
        .read_reg1(IF_ID_read_reg1),
        .read_reg2(IF_ID_read_reg2)
        );
    Controler  Ctrl_Unit (
        // Input:
        .OPcode(IF_ID_inst_in[6:0]),
        .Fun1(IF_ID_inst_in[14:12]),
        .Fun2(IF_ID_inst_in[31:25]),
        .zero(zero),
        // Output:
        .ALUSrc_A(ALUSrc_A),
        .ALUSrc_B(ALUSrc_B[1:0]),
        .ALU_Control(ALU_Control[4:0]),
        .Branch(Branch[1:0]),
        .DatatoReg(DatatoReg[1:0]),
        .mem_w(IF_ID_mem_w),
        .RegWrite(RegWrite),
        .B_H_W(B_H_W),                  // not used yet
        .sign(sign)                     // not used yet
        );

    Regs U2 (.clk(clk),
             .rst(rst),
             .L_S(MEM_WB_RegWrite),             // From Write-Back stage
             .R_addr_A(IF_ID_inst_in[19:15]),   // ID
             .R_addr_B(IF_ID_inst_in[24:20]),   // ID
             .Wt_addr(Wt_addr[4:0]),            // From Write-Back stage
             .Wt_data(Wt_data[31:0]),           // From Write-Back stage
             .rdata_A(rdata_A[31:0]),
             .rdata_B(rdata_B[31:0])
             );
    SignExt _signed_ext_ (.inst_in(IF_ID_inst_in), .imm_32(Imm_32));

    Mux2to1b32  _alu_source_A_ (
        .I0(rdata_A[31:0]),
        .I1(Imm_32[31:0]),   // not used 
        .s(ALUSrc_A),
        .o(ALU_A[31:0])
        );

    Mux4to1b32  _alu_source_B_ (
        .I0(rdata_B[31:0]),
        .I1(Imm_32[31:0]),
        .I2(),
        .I3(),
        .s(ALUSrc_B[1:0]),
        .o(ALU_B[31:0]
        ));
    assign IF_ID_Data_out = rdata_B;
    ID_Zero_Generator _id_zero_ (.A(ALU_A), .B(ALU_B), .ALU_operation(ALU_Control), .zero(zero));

    REG_ID_EXE _id_exe_ (
        .clk(clk), .rst(rst), .CE(V5), .ID_EXE_dstall(ID_EXE_dstall),
        // Input
        .inst_in(IF_ID_inst_in),
        .PC(IF_ID_PC),
        //// To EXE stage, ALU Operands A & B
        .ALU_A(ALU_A),
        .ALU_B(ALU_B),
        //// To EXE stage, ALU operation control signal
        .ALU_Control(ALU_Control),
        //// To MEM stage, for sw instruction, data from rs2 register written into memory
        .Data_out(IF_ID_Data_out),
        //// To MEM stage, for sw instruction, memor write enable signal
        .mem_w(IF_ID_mem_w),
        //// To WB stage, for choosing different data written back to register file
        .DatatoReg(DatatoReg),
        //// To WB stage, register file write valid
        .RegWrite(RegWrite),
        //// For Data Hazard
        .written_reg(IF_ID_written_reg), .read_reg1(IF_ID_read_reg1), .read_reg2(IF_ID_read_reg2),
        
        // Output
        .ID_EXE_inst_in(ID_EXE_inst_in),
        .ID_EXE_PC(ID_EXE_PC),
        .ID_EXE_ALU_A(ID_EXE_ALU_A),
        .ID_EXE_ALU_B(ID_EXE_ALU_B),
        .ID_EXE_ALU_Control(ID_EXE_ALU_Control),
        .ID_EXE_Data_out(ID_EXE_Data_out),
        .ID_EXE_mem_w(ID_EXE_mem_w),
        .ID_EXE_DatatoReg(ID_EXE_DatatoReg),
        .ID_EXE_RegWrite(ID_EXE_RegWrite),
        //// For Data Hazard
        .ID_EXE_written_reg(ID_EXE_written_reg), .ID_EXE_read_reg1(ID_EXE_read_reg1), .ID_EXE_read_reg2(ID_EXE_read_reg2)
        );

    // EXE:-------------------------------------------------------------------------------------------
    // From ID:
    //   1. inst_in
        //   Control_signals {
        //   2. ALU_Control (stops here)
        //   3. mem_w
        //   4. DatatoReg
        //   5. RegWrite
        //   }
    //   6. ALU_A (stops here)
    //   7. ALU_B (stops here)
    //   8. Data_out
    //   9. PC
    // Control Signals:
    //   1. ALU_Control
    // References:
    //   None
    // Pass-on:
    //   1. inst_in
        //   Control_signals {
        //   2. DatatoReg (WB)
        //   3. mem_w (MEM)
        //   4. RegWrite (WB)
        //   }
    //   5. Data_out (used at MEM together with mem_w)
    //   6. ALU_out (Addr_out outside) (used at both MEM and WB)
    //   7. PC
    // Out:
    //   None

    ALU _alualu_ (
        .A(ID_EXE_ALU_A[31:0]),
        .B(ID_EXE_ALU_B[31:0]),
        .ALU_operation(ID_EXE_ALU_Control[4:0]),
        .res(ID_EXE_ALU_out[31:0]),
        .overflow(),
        .zero()
        ); 

    REG_EXE_MEM _exe_mem_ (
        .clk(clk), .rst(rst), .CE(V5),
        // Input
        .inst_in(ID_EXE_inst_in),
        .PC(ID_EXE_PC),
        //// To MEM stage
        .ALU_out(ID_EXE_ALU_out),
        .Data_out(ID_EXE_Data_out),
        .mem_w(ID_EXE_mem_w),
        //// To WB stage
        .DatatoReg(ID_EXE_DatatoReg),
        .RegWrite(ID_EXE_RegWrite),
        
        .written_reg(ID_EXE_written_reg), .read_reg1(ID_EXE_read_reg1), .read_reg2(ID_EXE_read_reg2),
        
        // Output
        .EXE_MEM_inst_in(EXE_MEM_inst_in),
        .EXE_MEM_PC(EXE_MEM_PC),
        .EXE_MEM_ALU_out(EXE_MEM_ALU_out),
        .EXE_MEM_Data_out(EXE_MEM_Data_out),
        .EXE_MEM_mem_w(EXE_MEM_mem_w),
        .EXE_MEM_DatatoReg(EXE_MEM_DatatoReg),
        .EXE_MEM_RegWrite(EXE_MEM_RegWrite),
        
        .EXE_MEM_written_reg(EXE_MEM_written_reg), .EXE_MEM_read_reg1(EXE_MEM_read_reg1), .EXE_MEM_read_reg2(EXE_MEM_read_reg2)
        );

    // MEM:-------------------------------------------------------------------------------------------
    // From EXE:
    //   1. inst_in
        //   Control_signals {
        //   2. DatatoReg (WB)
        //   3. mem_w (stops here)
        //   4. RegWrite (WB)
        //   }
    //   5. Data_out (stops here)
    //   6. ALU_out (Addr_out outside) (used at both MEM and WB)
    //   7. PC
    // Control Signals:
    //   1. mem_w
    // Pass-on:
    //   1. inst_in
        //   Control_signals {
        //   2. DatatoReg (WB)
        //   3. RegWrite (WB)
        //   }
    //   4. ALU_out (Addr_out outside) (used at both MEM and WB)
    //   5. PC
    //   6. Data_in
    // Out:
    //   Data_out & mem_w, ALU_out(as Addr_out)
    
    REG_MEM_WB _mem_wb_ (
        .clk(clk), .rst(rst), .CE(V5),
        // Input
        .inst_in(EXE_MEM_inst_in),
        .PC(EXE_MEM_PC),
        .ALU_out(EXE_MEM_ALU_out),
        .DatatoReg(EXE_MEM_DatatoReg),
        .RegWrite(EXE_MEM_RegWrite),
        //// Comes from data memory
        .Data_in(data_in),
        
        // Output
        .MEM_WB_inst_in(MEM_WB_inst_in),
        .MEM_WB_PC(MEM_WB_PC),
        .MEM_WB_ALU_out(MEM_WB_ALU_out),
        .MEM_WB_DatatoReg(MEM_WB_DatatoReg),
        .MEM_WB_RegWrite(MEM_WB_RegWrite),
        .MEM_WB_Data_in(MEM_WB_Data_in)
        );

    // WB:-------------------------------------------------------------------------------------------
    // From EXE:
    //   1. inst_in
       //   Control_signals {
       //   2. DatatoReg (WB)
       //   3. RegWrite (WB)
       //   }
    //   4. ALU_out (Addr_out outside) (used at both MEM and WB)
    // Local:
    wire [31:0] LoA_data;

    assign Wt_addr[4:0] = MEM_WB_inst_in[11:7]; // rd, except for branch and store instructions
    LUI_or_AUIPC _loa_ (
        .inst_in(MEM_WB_inst_in[31:0]),
        .PC(MEM_WB_PC),
        .data(LoA_data[31:0])
        );
    Mux4to1b32  MUX3 (
        .I0(MEM_WB_ALU_out[31:0]),          // Others
        .I1(MEM_WB_Data_in[31:0]),          // Load
        .I2(LoA_data[31:0]),                // LUI and AUIPC
        .I3(MEM_WB_PC[31:0] + 32'b0100),    // jal and jalr: PC + 4
        .s(MEM_WB_DatatoReg[1:0]),
        .o(Wt_data[31:0]));
    
endmodule
