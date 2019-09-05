//comments
//1/2 counter
//comment region

module counter_template (

input wire 			clock,
input wire 			reset,
``IF ONE_FORTH_COUNTER_ENABLE
output reg [3:0] one_forth_freq,
``ENDIF
output reg [3:0] 	one_half_freq

);

always @(posedge clock, negedge reset) begin
	if (!reset) begin
		one_half_freq <= 4'h0
	end
	else begin
		one_half_freq <= one_half_freq + 1'b1;
	end
end

``IF ONE_FORTH_COUNTER_ENABLE
always @(posedge clock, negedge reset) begin
	if (!reset) begin
		one_forth_freq <= 4'h0
	end
	else begin
		one_forth_freq <= one_forth_freq + 1'b1;
	end
end
``ENDIF