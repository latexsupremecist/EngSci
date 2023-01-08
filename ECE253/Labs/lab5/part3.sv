module part3 #(parameter CLOCK_FREQUENCY = 500)(input logic ClockIn, Reset, Start, input logic [2:0] Letter,
            output logic DotDashOut, NewBitOut);
    
    logic [12:0] seq;
    always_comb begin
        case (Letter)
            0 : seq = 12'b101110000000;
            1 : seq = 12'b111010101000;
            2 : seq = 12'b111010111010;
            3 : seq = 12'b111010100000;
            4 : seq = 12'b100000000000;
            5 : seq = 12'b101011101000;
            6 : seq = 12'b111011101000;
            7 : seq = 12'b101010100000;
        endcase
    end
    
    logic w1, w2;

    RateDivider #(CLOCK_FREQUENCY) u0(ClockIn, Reset, w1);

    logic [12:0] Q;
    logic [3:0] CounterValue;

    assign DotDashOut = Q[12];
    assign w2 = (CounterValue != 12) ? w1 : 0;

    shiftmorse #(12) u1(ClockIn, Reset, !Start, w1, {0,seq}, Q);
    DisplayCounter u2(ClockIn, Reset, Start, w1, CounterValue);
    
    always_ff@(posedge ClockIn)
	begin
       	 if (w2 == 1)
            NewBitOut <= 1;
       	 else
            NewBitOut <= 0;
    	end
endmodule

module DisplayCounter(input logic Clock, Reset, Start, EnableDC, output logic [3:0] CounterValue);
    always_ff@(posedge Clock)
    begin
        if (Reset == 1)
            CounterValue <= 12;
        else if (Start == 1)
            CounterValue <= 0;
        else if (EnableDC == 1)
        begin
            if (CounterValue != 12)
                CounterValue <= CounterValue + 1;
        end
    end
endmodule

module RateDivider #(parameter CLOCK_FREQUENCY = 500)(input logic ClockIn, Reset,
            output logic Enable);
    logic [$clog2(CLOCK_FREQUENCY)-1:0] count, max;
	
	assign max = (CLOCK_FREQUENCY>>1)-1;
    assign Enable = (count == 'b0) ? '1 : '0;
    always_ff@(posedge ClockIn)
    begin
        if (Reset == 1)
            count <= max;
        else
		count <= (count == 0) ? max : count - 1;
    end
endmodule

module shiftmorse #(parameter N = 12)(clock, reset, load, shift, morse, Q);
    input logic clock, reset, load, shift;
    input logic[N:0] morse;
    output logic[N:0] Q;
    
    always_ff @ (posedge clock)
        begin
            if (reset == 1)
                Q <= 0;
            else if (load == 0)
                Q <= morse;
            	else if(shift == 1)
               		Q <= {Q[N-1:0], 1'b0};
        end
endmodule
