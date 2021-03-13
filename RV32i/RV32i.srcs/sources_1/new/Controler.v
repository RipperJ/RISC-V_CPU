`timescale 1ps / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/03/10 21:16:48
// Design Name: 
// Module Name: Controler
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


module Controler(
		input [6:0] OPcode,
		input [2:0] Fun1,
		input [6:0] Fun2,
		input wire zero,
		output reg ALUSrc_A,
		output reg [1:0] ALUSrc_B,
		output reg [1:0] DatatoReg,
		output reg [1:0] Branch,
		output reg RegWrite,
		output reg mem_w,
		output reg [4:0] ALU_Control,
		output reg [1:0] B_H_W,
		output reg sign
		);
	always @(*) begin
		ALUSrc_B = 0;
		ALUSrc_A = 0;
		DatatoReg = 2'b0;
		Branch = 0;
		RegWrite = 0;
		mem_w = 0;
		B_H_W = 2'b0; // default: immediate is a word
		sign = 1'b1; // default: signed extension to "write_data"
		case(OPcode)
		    // R
			7'b0110011: begin 
				RegWrite = 1;
				case(Fun1)
				    3'b000: begin
				        case (Fun2)
				            7'b0000000: ALU_Control = 5'b00010; // ADD
				            7'b0100000: ALU_Control = 5'b00011; // SUB
				            default: ALU_Control = 5'b11111;
				        endcase
				    end
				    3'b001: begin // SLL
				        ALU_Control = 5'b00111;
				    end
				    3'b010: ALU_Control = 5'b00101; // SLT
				    3'b011: ALU_Control = 5'b00110; // SLTU
				    3'b100: ALU_Control = 5'b00100; // XOR
				    3'b101: begin
				        case (Fun2)
				            7'b0000000: begin // SRL
                                ALU_Control = 5'b01000;
                            end
                            7'b0100000: begin // SRA
                                ALU_Control = 5'b01001;
                            end
                            default: ALU_Control = 5'b11111;
				        endcase
				    end
				    3'b110: ALU_Control = 5'b00001; // OR
				    3'b111: ALU_Control = 5'b00000; // AND
					default: ALU_Control = 5'b11111;
				endcase
			end
			// I
			7'b0010011: begin
			    RegWrite = 1;
			    case (Fun1)
			        3'b000: begin
			            ALU_Control = 5'b00010; // ADDI                   
                        ALUSrc_B = 2'b01;    
			        end
			        3'b010: begin
			            ALU_Control = 5'b00101; // SLTI
			            ALUSrc_B = 2'b01;
			        end
			        3'b011: begin
			            ALU_Control = 5'b00110; // SLTIU
                        ALUSrc_B = 2'b01;
			        end
			        3'b100: begin
                        ALU_Control = 5'b00100; // XORI
                        ALUSrc_B = 2'b01;
			        end
			        3'b110: begin
                        ALU_Control = 5'b00001; // ORI
                        ALUSrc_B = 2'b01;
			        end
			        3'b111: begin
                        ALU_Control = 5'b00000; // ANDI
                        ALUSrc_B = 2'b01; 
			        end
			        3'b001: begin
			            ALU_Control = 5'b00111; // SLLI
                        ALUSrc_B = 2'b01;
			        end
			        3'b101: begin
			            ALUSrc_B = 2'b01;
			            case (Fun2)
			                7'b0000000: ALU_Control = 5'b01000; // SRLI
			                7'b0100000: ALU_Control = 5'b01001; // SRAI
			            endcase
			        end
			    endcase
			end
			7'b0000011: begin	// l
				ALU_Control = 5'b00010;
				ALUSrc_B = 2'b01;
				DatatoReg = 2'b01;
				RegWrite = 1;
				case (Fun1)
				    3'b000: begin // LB
				        B_H_W = 2'b01; // byte
				    end
				    3'b001: begin // LH
				        B_H_W = 2'b10; // half word
				    end
				    3'b100: begin // LBU
				        B_H_W = 2'b01; // byte
				        sign = 1'b0;
				    end
				    3'b101: begin // LHU
				        B_H_W = 2'b10; // half word
				        sign = 1'b0;
				    end
				    // 3'b010:; // LW
				endcase
			end
			7'b0100011: begin   // S
			    ALU_Control = 5'b00010;
			    ALUSrc_B = 2'b01;
			    mem_w = 1;
			    case (Fun1)
			        3'b000: begin
			            B_H_W = 2'b01; // byte
			        end
			        3'b001: begin
			            B_H_W = 2'b10; // half word
			        end
			        // 3'b010: ; // SW
			    endcase
			end
			7'b1100011: begin	// Branch
			    case (Fun1)
			        3'b000: begin // BEQ
			            ALU_Control = 5'b00011; 
			            Branch = {1'b0, zero};
			        end 
			        3'b001: begin // BNE
			            ALU_Control = 5'b00011;
			            Branch = {1'b0, ~zero};
			        end
			        3'b100: begin // BLT
			            ALU_Control = 5'b00101;
			            Branch = {1'b0, zero};
			        end
			        3'b101: begin // BGE
			            ALU_Control = 5'b01010;
			            Branch = {1'b0, zero};
			        end
			        3'b110: begin // BLTU
			            ALU_Control = 5'b00110;
			            Branch = {1'b0, zero}; 
			        end
			        3'b111: begin // BGEU
			            ALU_Control = 5'b01011;
			            Branch = {1'b0, zero};
			        end
			    endcase
			end
			7'b1101111: begin	// jal
				Branch = 2'b10;
				DatatoReg = 2'b11;
				RegWrite = 1;
			end
            7'b1100111: begin   // jalr
                Branch = 2'b11;
                DatatoReg = 2'b11;
                RegWrite = 1;
            end
            7'b0110111: begin    // lui
                DatatoReg = 2'b10;
                RegWrite = 1;
            end
            7'b0010111: begin   // AUIPC
                DatatoReg = 2'b10;
                RegWrite = 1;
            end
			default: ALU_Control = 5'b11111;
		endcase
	end
endmodule

