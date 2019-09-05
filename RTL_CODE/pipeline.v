//comments
//1/2 counter
//comment region

module pipeline (

input wire 			clock,
input wire 			reset,
``IF ONE_FORTH_COUNTER_ENABLE
input wire one_forth_pipe_enable,
input wire signal_from_one_forth,
output reg one_forth_pipeline,
``ENDIF
input wire signal_from_one_half,
input wire one_half_pipe_enable,
output reg one_half_pipeline
);

always @(posedge clock, negedge reset) begin
	if (!reset) begin
		one_half_pipeline <= 1'b0;
	end
	else begin
		if (one_half_pipe_enable) begin
			one_half_pipeline <= signal_from_one_half;
		end
	end
end

``IF ONE_FORTH_COUNTER_ENABLE
always @(posedge clock, negedge reset) begin
	if (!reset) begin
		one_forth_pipeline <= 1'b0;
	end
	else begin
		if (one_forth_pipe_enable) begin
			one_forth_pipeline <= signal_from_one_forth;
		end
	end
end
``ENDIF