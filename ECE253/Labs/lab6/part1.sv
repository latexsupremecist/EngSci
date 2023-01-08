    module part1(
        input logic Clock,
        input logic Reset,
        input logic w,
        output logic z,
        output logic [3:0] CurState
    );
        
        // Enum allows you to use names for numerical values, such as state encodings.
        // With enums, you will see the names (e.g., A) in the waveform, instead of
        // the state encoding (e.g., 0000), which makes debug easier.         
        typedef enum logic [3:0] {A = 4'd0, 
                                  B = 4'd1, 
                                  C = 4'd2, 
                                  D = 4'd3, 
                                  E = 4'd4, 
                                  F = 4'd5, 
                                  G = 4'd6} statetype;
                                  
        statetype y_Q, Y_D; // y_Q represents current state, Y_D represents next state

        //State table
        //The state table should only contain the logic for state transitions
        //Do not mix in any output logic. The output logic should be handled separately.
        //This will make it easier to read, modify and debug the code.
        always_comb begin
            case (y_Q)
                A: begin
                       if (!w) Y_D = A;
                       else Y_D = B;
                   end
	   	        B: begin
                        if (!w) Y_D = A;
                        else Y_D = C;
                    end
                C: begin
                        if (!w) Y_D = E;
                        else Y_D = D;
                    end
                D: begin
                        if (!w) Y_D = E;
                        else Y_D = F; 
                    end
                E: begin
                        if (!w) Y_D = A;
                        else Y_D = G; 
                end
                F: begin
                        if (!w) Y_D = E;
                        else Y_D = F; 
                    end
                G: begin
                        if (!w) Y_D = A;
                        else Y_D = C; 
                    end
                default: begin
                            if (!w) Y_D = A;
                            else Y_D = B;
                end
            endcase
        end // state_table

        // State Registers
        always_ff @(posedge Clock) begin
            if(Reset == 1'b1)
                y_Q <= A;
            else
                y_Q <= Y_D;
        end // state_FFS

        // Output logic
        // Set out_light to 1 to turn on LED when in relevant states
        assign z = ((y_Q == F) | (y_Q == G));

        assign CurState = y_Q;        
    endmodule
    
    
