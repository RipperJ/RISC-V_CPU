`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 19:39:55
// Design Name: 
// Module Name: REG32
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


module REG32(
    input clk,
    input rst,
    input CE,
    input [31:0] D,
    output reg [31:0] Q = 0,
    input PC_dstall
    );
    
    always @ (posedge clk or posedge rst) begin
	    if (rst == 1) Q <= 32'h00000000;
	    if (PC_dstall == 0) begin
		    if (rst == 1) Q <= 32'h00000000;
		    else if (CE) Q <= D;
		end
    end
    
endmodule
