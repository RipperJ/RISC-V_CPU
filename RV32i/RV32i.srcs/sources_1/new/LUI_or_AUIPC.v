`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 22:56:35
// Design Name: 
// Module Name: LUI_or_AUIPC
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


module LUI_or_AUIPC(
        input [31:0] inst_in,
        input [31:0] PC,
        output reg [31:0] data
    );
    always @ (*) begin
        data = 32'h0;
        case (inst_in[6:0])
            7'b0110111: data = {inst_in[31:12], 12'b0};
            7'b0010111: data = {inst_in[31:12], 12'b0} + PC;
        endcase
    end
        
endmodule
