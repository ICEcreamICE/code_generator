//Registers which has W/R bus that can be access from a certain master
/// #start python code inside verilog RTL file
```ADDR_MSB = 32
```ADDR_LSB = 0
```ADDR_WIDTH = ADDR_MSB - ADDR_LSB + 1
```WRITE_DATA_MSB = 32
```WRITE_DATA_LSB = 0
```READ_DATA_LSB = 20
```READ_DATA_MSB = 0
```ONE_HALF_WIDTH = 16
```ONE_FORTH_WIDTH = 8
```ONE_HALF_ADDR = "AA"
```ONE_FORTH_ADDR = "55"
```ONE_HALF_READ_ZREO_WIDTH = READ_DATA_MSB - ONE_HALF_WIDTH + 1
```ONE_FORTH_READ_ZREO_WIDTH = READ_DATA_MSB - ONE_FORTH_WIDTH + 1
```ONE_FORTH_COUNTER_ENABLE = False
```prefix = "EngineTEST"

module ``{prefix}_controlling_register(
input wire clock,
input wire reset,
input wire [``{ADDR_MSB} : ``{ADDR_LSB}] address,
input wire write_enable,
input wire [``{WRITE_DATA_MSB} : ``{WRITE_DATA_LSB}] write_data,
input wire read_enalbe,
output reg [``{READ_DATA_MSB} : ``{READ_DATA_LSB}] read_data,
``IF {ONE_FORTH_COUNTER_ENABLE}
output reg one_forth_pipe_enable,
``ENDIF
output reg one_half_pipe_enalbe,
```for i in range(3):
````p  f"input wire for_test_{i},\n"

``FOR {i in range(3)}
	``IF {i==2}
output reg if_test_``{i}
	``ELSE
output reg else_test_``{i},
	``ENDIF
``ENDFOR
);

always @(posedge clock, negedge reset) begin
  if (!reset) begin
    one_half_pipe_enable <= ``{ONE_HALF_WIDTH}'h0;
  end
  else begin
    if ((address == ``{ADDR_WIDTH}'h``{ONE_HALF_ADDR}) && write_enable) begin
      one_half_pipe_enable <= #1 write_data[``{ONE_HALF_WIDTH} - 1 : 0];
    end
  end
end

``IF {ONE_FORTH_COUNTER_ENABLE}
always @(posedge clock, negedge reset) begin
  if (!reset) begin
    one_forth_pipe_enalbe <= ``{ONE_HALF_WIDTH}'h0;
  end
  else begin
    if ((address == ``{ADDR_WIDTH}'h``{ONE_FORTH_ADDR}) && write_enable) begin
      one_forth_pipe_enable <= #1 write_data[0];
    end
  end
end
``ENDIF

always @* begin
  if ((address == ``{ADDR_WIDTH}'h``{ONE_HALF_ADDR}) && read_enable) begin
    read_data = {``{ONE_HALF_READ_ZREO_WIDTH}'h0, one_half_pipe_enable};
  end
``IF {ONE_FORTH_COUNTER_ENABLE}
	else if ((address == ``{ADDR_WIDTH}'h``{ONE_FORTH_ADDR}) && read_enable) begin
	   read_data = {``{ONE_FORTH_READ_ZREO_WIDTH}'h0, one_forth_pipe_enable};
	end
	``ELSE
		assign read_data = {``{ONE_FORTH_READ_ZREO_WIDTH}'h0, one_forth_pipe_enable};
``ENDIF
end

//AUTOINST test_module_1
test_module_1 i_test_module_1 (
)

endmodule

module test_module_1 (
  input a,
  input b,
  output c
)
``FOR {o in range(2)}
param TEST_MODULE_1_PARAM``{o}
``ENDFOR

endmodule