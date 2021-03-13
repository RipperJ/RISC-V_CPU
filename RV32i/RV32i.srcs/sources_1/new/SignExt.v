`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 21:48:13
// Design Name: 
// Module Name: SignExt
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


module SignExt(
    input [31:0] inst_in,
    output reg [31:0] imm_32
    );
    
    always @ (*) begin
        imm_32 = 0;
        case (inst_in[6:0]) 
            // L
            7'b0000011: begin
                imm_32 = {{20{inst_in[31]}}, inst_in[31:20]};
            end
            // I
            7'b0010011: begin
                case (inst_in[14:12])
                    // slli, srli, srai: unsigned
                    3'b001, 3'b101: begin
                        imm_32 = {27'b0, inst_in[24:20]};
                    end
                    // other I instructions
                    default: begin
                        imm_32 = {{20{inst_in[31]}}, inst_in[31:20]};
                    end
                endcase
            end
            // SB, SH, SW
            7'b0100011: begin 
                imm_32 = {{20{inst_in[31]}}, inst_in[31:25], inst_in[11:7]};
            end
            // Branch
            7'b1100011: begin
                imm_32 = {{19{inst_in[31]}}, inst_in[31], inst_in[7], inst_in[30:25], inst_in[11:8], 1'b0};
            end
        endcase
    end
    
endmodule
