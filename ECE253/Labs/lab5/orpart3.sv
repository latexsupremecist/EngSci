module halfsecond
#(parameter CLOCK_FREQUENCY=4)(
input logic ClockIn,
input logic Reset,
output logic half
);

logic[$clog2(CLOCK_FREQUENCY)-1:0] counter, max;
assign max = (CLOCK_FREQUENCY>>1)-1;

always_ff @(posedge ClockIn)
begin
	half <= (counter == 'b0) ? 'b1 : 'b0;
	if(Reset)
		counter <= max;
	else
		counter <= (counter == 'b0) ? max : counter - 1;
end
endmodule

module twelve(input logic half, Reset, output logic[3:0] period);
always_ff @(posedge half)
begin
	if(Reset)
		period <= 4'b0010;
	else
		period <= (period == 4'b0000) ? 4'b1011 : period - 1;
end
endmodule

module subcircuit(input logic a, half, output logic b);

    always_ff @(posedge half)
    begin
        b <= a;
    end
endmodule

module loadmorse(input logic Start, half,input logic[3:0] period, input logic[2:0] Letter, output logic DotDashOut, check);

logic [11:0] A, B, C, D, E, F, G, H, morse;

assign A = 12'b101110000000;
assign B = 12'b111010101000;
assign C = 12'b111010111010;
assign D = 12'b111010100000;
assign E = 12'b100000000000;
assign F = 12'b101011101000;
assign G = 12'b111011101000;
assign H = 12'b101010100000;

always_ff @(posedge half)
if(period == 'b0)
begin
    case(Letter)
    0: morse <= A;
    1: morse <= B;
    2: morse <= C;
    3: morse <= D;
    4: morse <= E;
    5: morse <= F;
    6: morse <= G;
    7: morse <= H;
    endcase
	check <= 1;
end

subcircuit u0(morse[10], half, morse[11]);
subcircuit u1(morse[9], half, morse[10]);
subcircuit u2(morse[8], half, morse[9]);
subcircuit u3(morse[7], half, morse[8]);
subcircuit u4(morse[6], half, morse[7]);
subcircuit u5(morse[5], half, morse[6]);
subcircuit u6(morse[4], half, morse[5]);
subcircuit u7(morse[3], half, morse[4]);
subcircuit u8(morse[2], half, morse[3]);
subcircuit u9(morse[1], half, morse[2]);
subcircuit u10(morse[0], half, morse[1]);

assign DotDashOut = morse[11];
endmodule


module part3
#(parameter CLOCK_FREQUENCY=4)(
input logic ClockIn,
input logic Reset,
input logic Start,
input logic [2:0] Letter,
output logic DotDashOut,
output logic NewBitOut
);

logic half;

halfsecond u0(ClockIn, Reset, half);
loadmorse u1(Start, half, period, Letter, DotDashOut, check);
twelve u2(half, Reset, period);
always_ff @(posedge ClockIn)
begin
    if(!Reset && check)
    begin
        NewBitOut <= half;
    end
end
endmodule
