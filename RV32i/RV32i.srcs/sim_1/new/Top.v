`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/12 09:23:35
// Design Name: 
// Module Name: Top
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


module Top;

    reg clk;
    reg rst;
    
    reg [31:0] Inst_ROM[0:16383];
    reg [31:0] Data_RAM[0:16383];
    
    wire [31:0] data_in;
    wire [31:0] inst_in;
    
    wire [31:0] addr_out;   // ALU_out from CPU
    wire [31:0] data_out;   // data_out from CPU
    wire data_valid;        // mem_w from CPU
    wire [31:0] PC;

    integer i;
    integer j;
    
    RV32iPCPU _rv32ipcpu_ (
        .clk(clk),
        .rst(rst),
        .data_in(data_in),
        .inst_in(inst_in),
        
        .ALU_out(addr_out),
        .data_out(data_out),
        .mem_w(data_valid),
        .PC_out(PC)        
        );
    
    assign inst_in = Inst_ROM[PC[15:2]];
    assign data_in = Data_RAM[addr_out[15:2]];
    always @ (negedge clk or posedge rst) begin
        if (rst == 1'b1) begin                      // reset data memory
            for (j = 0; j < 16384; j = j + 1) begin
                Data_RAM[j] <= 32'h0;
            end
        end
        else begin
            if (data_valid == 1'b1) begin           // write data memory
                Data_RAM[addr_out[15:2]] <= data_out;
            end
        end
    end
        
    initial begin
        // Initialize Inst ROM and Data RAM
        $readmemh("ROM_data.txt", Inst_ROM);    // Please find this file in `....../[RV32i directory]/RV32i.sim/sim_1/behav/xsim/ROM_data.txt`
                                                   // When using "Assembler", you can get the hex numbers at the right-hand side text box
        for (i = 0; i < 16384; i = i + 1) begin
            Data_RAM[i] = 32'h0;
        end
        clk = 0;
        rst = 0;
        #1;
        rst = 1;
        #1;
        rst = 0;
        
    end 
    always begin
        clk = ~clk;
        #1;
        if (Data_RAM[0] == 32'b1) begin             // The first entry of data memory is set to 1 after execution, please check `....../[RV32i directory]/Vec_Mul.txt` assembly code
            $display("Simulation cycle count: %t\n", $time);
            $stop;
        end
    end

endmodule
