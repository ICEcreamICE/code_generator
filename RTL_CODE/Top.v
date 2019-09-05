//TOP level file
//use to instance(call) all modules to build up a CHIP

module top (
input wire clock,
input wire reset,
``IF ONE_FORTH_COUNTER_ENABLE
output wire pipe_out_one_forth_``$i, ``LOOP 2
``ENDIF
output wire pipe_out_one_half_0``$i, ``LOOP 2
input wire clock,
input wire reset,
input wire [``$ADDR_MSB : ``$ADDR_LSB] address,
input wire write_enable,
input wire [``$WRITE_DATA_MSB : ``$WRITE_DATA_LSB] write_data,
input wire read_enalbe,
output reg [``$READ_DATA_MSB : ``$READ_DATA_LSB] read_data
);

``IF ONE_FORTH_COUNTER_ENABLE
wire one_forth_pipe_enable;
``ENDIF
wire oue_half_pipe_enalbe;

counter_template u_counter_template ( //module instance method
	.clock (clock),
	.reset (reset),
``IF ONE_FORTH_COUNTER_ENABLE
	.one_forth_freq (one_forth_freq),
``ENDIF
	.one_half_freq (one_half_freq)
);

controlling_register u_controlling_register (
	.clock (clock),
	.reset (reset),
	.write_data (write_data),
	.write_enable (write_enable),
	.read_enable (read_enable),
	.read_data (read_data),
``IF ONE_FORTH_COUNTER_ENABLE
	.one_forth_pipe_enalbe (one_forth_pipe_enable),
``ENDIF
	.one_half_pipe_enable (one_half_pipe_enable)
);

``FOR (i=0, i<2, i++)
pipeline u_pipeline_``$i (
	.clock (clock),
	.reset (reset),
``IF ONE_FORTH_COUNTER_ENABLE
	.one_forth_pipe_enable (one_forth_pipe_enable),
	.signal_from_one_forth (one_forth_freq),
	.one_forth_pipeline (pipe_out_one_forth_``$i),
``ENDIF
	.one_half_pipe_enable (one_half_pipe_enable),
	.signal_from_one_half (one_half_freq),
	.one_half_pipeline (pipe_out_one_half_``$i)
);
``ENDFOR








