`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 19:39:55
// Design Name: 
// Module Name: ALU
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


module ALU(
	input [31:0] A,
	input [31:0] B,
	input [4:0] ALU_operation,
	output reg signed [31:0] res,
	output reg overflow,
	output wire zero
    );
	wire res_temp;
	assign res_temp = res;
	parameter one = 32'h00000001, zero_0 = 32'h00000000;
	wire signed [31:0] A_temp, B_temp;
	assign A_temp = A;
	assign B_temp = B;
	// always @ (A or B or ALU_operation) begin
    always @ (*) begin
		case (ALU_operation)
			5'b00000: begin	// and
				res = A & B;
				overflow = 0;
			end
			5'b00001: begin	// or
				res = A | B;
				overflow = 0;
			end
			5'b00010: begin	// add
				res = A_temp + B_temp;
				if ((A[31] == 1 && B[31] == 1 && res[31] == 0) || (A[31] == 0 && B[31] == 0 && res[31] == 1))
					overflow = 1;
				else overflow = 0;
			end
			5'b00011: begin	// sub
				res = A_temp - B_temp;
				if ((A[31] == 1 && B[31] == 0 && res[31] == 0) || (A[31] == 0 && B[31] == 1 && res[31] == 1))
					overflow = 1;
				else overflow = 0;
			end
            5'b00100: begin // XOR
                res = A ^ B;
                overflow = 0;
            end
			5'b00101: begin	// SLT
				res = (A_temp < B_temp) ? one : zero_0;
				overflow = 0;
			end
            5'b00110: begin // SLTU
                res = (A < B) ? one : zero_0;
                overflow = 0;
            end
            5'b00111: begin // SLL
                res = (A << B);
                overflow = 0;
            end
            5'b01000: begin // SRL
                res = (A >> B);
                overflow = 0;
            end
            5'b01001: begin // SRA
                res = (A_temp >> B);
                overflow = 0;
            end
			5'b01010: begin // BGE
                res = (A_temp >= B_temp) ? one : zero_0;
                overflow = 0;
            end
            5'b01011: begin // BGEU
                res = (A >= B) ? one : zero_0;
                overflow = 0;
            end
			default: res = 32'hx;
		endcase
	end
	assign zero = (res == 0) ? 1 : 0;

endmodule
