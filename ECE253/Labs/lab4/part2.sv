module part2(Clock, Reset_b, Data, Function, ALUout);

    input logic Clock, Reset_b;
    input logic[1:0] Function;
    input logic[3:0] Data;
    output logic[7:0] ALUout;

    always_ff @(posedge Clock)
    begin
        case ({Reset_b, Function})
        0: ALUout <= (ALUout[3:0] + Data);
        1: ALUout <= (ALUout[3:0] * Data);
        2: ALUout <= (ALUout[3:0] << Data);
        3: ALUout <= ALUout;
        default: ALUout <= 8'b00000000;
        endcase
    end

endmodule
