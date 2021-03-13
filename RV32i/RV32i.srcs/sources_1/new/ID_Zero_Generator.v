`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 23:29:53
// Design Name: 
// Module Name: ID_Zero_Generator
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


module ID_Zero_Generator(
	input [31:0] A, 
	input [31:0] B,
	input [4:0] ALU_operation,
	output zero
    );
    reg [31:0] res;
	parameter one = 32'h00000001, zero_0 = 32'h00000000;
	wire signed [31:0] A_temp, B_temp;
	assign A_temp = A;
	assign B_temp = B;
	
	always @ (*) begin // A or B or ALU_operation
		case (ALU_operation)
			5'b00011: begin	// sub
				res = A_temp - B_temp;
			end
			5'b00101: begin // BLT
			    res = (A_temp < B_temp) ? zero_0 : one;
			end
            5'b01010: begin // BGE
                res = (A_temp >= B_temp) ? zero_0 : one;
            end
            5'b00110: begin // BLTU
                res = (A < B) ? zero_0 : one;
            end
            5'b01011: begin // BGEU
                res = (A >= B) ? zero_0 : one;
            end
			default: res = 32'hz;
		endcase
	end
	assign zero = (res == 0) ? 1 : 0;

endmodule

