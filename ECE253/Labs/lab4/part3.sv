module subcircuit(Loadleft, D, loadn, right, left, reset, clock, Q);
    input logic Loadleft, D, loadn, right, left, reset, clock;
    output logic Q;

    always_ff @(posedge clock)
    begin
        if (reset) Q <= 1'b0;
        else Q <= loadn ? (Loadleft ? left : right) : D;
    end
endmodule

module part3(clock, reset, ParallelLoadn, RotateRight, ASRight, Data_IN, Q);
    input logic clock, reset, ParallelLoadn, RotateRight, ASRight;
    input logic[3:0] Data_IN;
    output logic[3:0] Q;
    logic x;

    subcircuit u0(RotateRight, Data_IN[3], ParallelLoadn, Q[2], Q[0], reset, clock, x);
    assign Q[3] = (ParallelLoadn && RotateRight && ASRight) ? Q[3] : x;
    subcircuit u1(RotateRight, Data_IN[2], ParallelLoadn, Q[1], Q[3], reset, clock, Q[2]);
    subcircuit u2(RotateRight, Data_IN[1], ParallelLoadn, Q[0], Q[2], reset, clock, Q[1]);
    subcircuit u3(RotateRight, Data_IN[0], ParallelLoadn, Q[3], Q[1], reset, clock, Q[0]);
endmodule