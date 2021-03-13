`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 21:36:08
// Design Name: 
// Module Name: Get_rw_regs
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


module Get_rw_regs(
        input [31:0] inst_in,
        output reg [4:0] written_reg,
        output reg [4:0] read_reg1,
        output reg [4:0] read_reg2
    );
    always @ (*) begin
        written_reg = 5'b00000;
        read_reg1 = 5'b00000;
        read_reg2 = 5'b00000;
        case (inst_in[6:0]) 
            7'b0110111, 7'b0010111, 7'b1101111: begin // LUI, AUIPC, JAL
                written_reg = inst_in[11:7];
            end
            // JALR
            // L
            // I
            7'b1100111,
            7'b0000011,
            7'b0010011: begin
                written_reg = inst_in[11:7];
                read_reg1 = inst_in[19:15];
            end
            // BEQ, BNE, BLT, BGE, BLTU, BGEU
            // SB, SH, SW
            7'b1100011,
            7'b0100011: begin 
                read_reg1 = inst_in[19:15];
                read_reg2 = inst_in[24:20];
            end
            7'b0110011: begin // R
                written_reg = inst_in[11:7];
                read_reg1 = inst_in[19:15];
                read_reg2 = inst_in[24:20];
            end
        endcase
    end
endmodule
