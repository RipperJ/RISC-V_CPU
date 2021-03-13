`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 19:39:55
// Design Name: 
// Module Name: Mux2to1b32
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


module Mux2to1b32(
		input s,
		input [31:0] I0,
		input [31:0] I1,
		output [31:0] o
    );
	assign o = s ? I1 : I0;

endmodule