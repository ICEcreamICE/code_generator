//Registers which has W/R bus that can be access from a certain master 
/// #start python code inside verilog RTL file 
 
module EngineTEST_controlling_register(
input wire clock, 
input wire reset, 
input wire [32 : 0] address,
input wire write_enable, 
input wire [32 : 0] write_data,
input wire read_enalbe, 
output reg [0 : 20] read_data,
output reg one_half_pipe_enalbe, 
input wire for_test_0,
input wire for_test_1,
input wire for_test_2,
 
output reg else_test_0,
output reg else_test_1,
output reg if_test_2
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
 
 
always @* begin 
  if ((address == 33'hAA) && read_enable) begin
    read_data = {-15'h0, one_half_pipe_enable};
  end 
		assign read_data = {-7'h0, one_forth_pipe_enable};
end 
 
//AUTOINST test_module_1 
test_module_1 i_test_module_1 ( 
); 
 
endmodule 
 
module test_module_1 ( 
.a (a[1:0]),
.b (b[`defM:`defL]),
.c (c),
.d (d)
); 
 
endmodule 
 
module test_module_1 ( 
  input wire [1:0] a, 
  input wire [`defM:`defL]b, 
  output wire c, 
  inout wire d 
); 
 
param TEST_MODULE_1_PARAM0,
param TEST_MODULE_1_PARAM1,
param TEST_MODULE_1_PARAM2,
param TEST_MODULE_3_PARAM3
 
endmodule 
