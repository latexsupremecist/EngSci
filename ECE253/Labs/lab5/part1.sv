module tflipflop(input logic Clock, input logic Enable, input logic Reset, output logic Q);
    always_ff @(posedge Clock)
    begin
        if(Reset)
            Q <= 0;
        else Q <= Enable ? ~Q : Q;
    end
endmodule
        
module part1(input logic Clock,
    input logic Enable,
    input logic Reset,
    output logic [7:0] CounterValue);

    tflipflop u0(Clock, Enable, Reset, CounterValue[0]);
    tflipflop u1(Clock, CounterValue[0], Reset, CounterValue[1]);
    tflipflop u2(Clock, &{Enable, CounterValue[1:0]}, Reset, CounterValue[2]);
    tflipflop u3(Clock, &{Enable, CounterValue[2:0]}, Reset, CounterValue[3]);
    tflipflop u4(Clock, &{Enable, CounterValue[3:0]}, Reset, CounterValue[4]);
    tflipflop u5(Clock, &{Enable, CounterValue[4:0]}, Reset, CounterValue[5]);
    tflipflop u6(Clock, &{Enable, CounterValue[5:0]}, Reset, CounterValue[6]);
    tflipflop u7(Clock, &{Enable, CounterValue[6:0]}, Reset, CounterValue[7]);

endmodule






