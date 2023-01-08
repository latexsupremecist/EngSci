module RateDivider
#(parameter CLOCK_FREQUENCY = 500) (
input logic ClockIn,
input logic Reset,
input logic [1:0] Speed,
output logic Enable
);

logic[$clog2(CLOCK_FREQUENCY)+1:0] counter, max;

always_ff @(posedge ClockIn)
begin
    case(Speed)
    0: max <= 'b0;
    1: max <= CLOCK_FREQUENCY-1;
    2: max <= 2*CLOCK_FREQUENCY-1;
    3: max <= 4*CLOCK_FREQUENCY-1;
    endcase
    assign Enable = (counter == 'b0) ? 'b1 : 'b0;
    if(Reset)
    assign counter = max;
    else
    assign counter = (counter == 'b0) ? max : counter - 1;

    
end
endmodule

module DisplayCounter (
input logic Clock,
input logic Reset,
input logic EnableDC,
output logic [3:0] CounterValue
);

always_ff @(posedge Clock)
    if(Reset) CounterValue <= 4'b0000;
    else begin
        if(EnableDC) CounterValue <= (CounterValue == 4'b1111) ? 4'b0000 : CounterValue + 1;
    end
endmodule

module part2
#(parameter CLOCK_FREQUENCY = 500)(
input logic ClockIn,
input logic Reset,
input logic [1:0] Speed,
output logic [3:0] CounterValue
);

logic Enable;

RateDivider u0(ClockIn, Reset, Speed, Enable);
DisplayCounter u1(ClockIn, Reset, Enable, CounterValue);
endmodule