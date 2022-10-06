## Lecture 13

### Midterm Information
- Letter sized aid sheet, both sides
- Anything goes (printed, handwritten, any information is allowed)
- 90 minutes
- Topics: A1-B2

### Flip Flops
- Gated D Latch
	- If clock is high: outputs D
	- If clock is low: outputs **stored value** of D, i.e. the value of D just before clock is low
- Positive edge triggered D-FF
	- If clock goes from low to high: outputs D
	- Else: outputs **stored value** of D
- Negative edge triggered D-FF
	- If clock goes from high to low: outputs D
	- Else: outpus **stored value** of D
**Clocks and D cannot change at the same time!**
- Register: a synonym for flip flop

### Verilog for D-latch
```
module D-latch(input logic D, clk, output logic Q);
	always_latch
		if (clk == 1)
			Q = D;
endmodule
```
In this case, latch stores `Q` when `clk` is not 1.

### Verilog code for flip flops
```
module D_FF(input logic D, clk, output logic Q);
	always_ff @(posedge clk)
		Q <= D;
endmodule
```
`posedge` is a keyword used to create flip flops. Similarly, `negedge` is a keyword that does the opposite. For flip flops, the assignments should use `<=` instead of `=`. From this example, `Q` only stores the value of `D` at positive clock edges.

### Verilog for register
8 bit input plus clock, 8 bit output
```
module reg8(input logic[7:0]D, input logic clk, output logic[7:0]Q);
	always_ff @(posedge clk)
		Q <= D;
endmodule
```

### Resets
- Synchronous: dependent on the clock edge
	- Replace D with reset AND D
```
module D_FF(input logic D, clk, resetn, output logic Q);
	always_ff @(posedge clk)
		if(resetn == 0)
			Q<=1'b0;
		else
			Q <= D;
endmodule
```
- Asynchronous: independent on the clock edge
	- Case 1: If `clk == 0`, `resetn == 0`, gives `Q = 0`
	- Case 2: If `clk == 1`, `resetn == 0`...

