//Registers which has W/R bus that can be access from a certain master 
/// #start python code inside verilog RTL file 
 
module controlling_register( 
input wire clock, 
input wire reset, 
input wire [32 : 0] address,
input wire write_enable, 
input wire [32 : 0] write_data,
input wire read_enalbe, 
output reg [0 : 20] read_data,
output reg one_forth_pipe_enable, 
output reg one_half_pipe_enalbe, 
input wire [0:0] for_test_0;
input wire [1:0] for_test_1;
input wire [2:0] for_test_2;
 
output reg test_0,
output reg test_1,
output reg test_2,
); 
 
always @(posedge clock, negedge reset) begin 
	if (!reset) begin 
		one_half_pipe_enable <= 16'h0;
	end 
	else begin 
		if ((address == 33'hAA) && write_enable) begin
			one_half_pipe_enable <= #1 write_data[16 - 1 : 0];
		end 
	end 
end 
 
always @(posedge clock, negedge reset) begin 
	if (!reset) begin 
		one_forth_pipe_enalbe <= 16'h0;
	end 
	else begin 
		if ((address == 33'h55) && write_enable) begin
			one_forth_pipe_enable <= #1 write_data[0]; 
		end 
	end 
end 
 
always @* begin 
	if ((address == 33'hAA) && read_enable) begin
		read_data = {-15'h0, one_half_pipe_enable};
	end 
	else if ((address == 33'h55) && read_enable) begin
	   read_data = {-7'h0, one_forth_pipe_enable};
	end 
end 
