## Lecture 19

### Lab 5
- Part 1: relatively straightforward
- Part 2: rate divider
	- Display value changes when counter counts to a specific number
	- Only when enable is set to 1
- Part 3: Morse Code Machine
	- Note when to shift

### Simple Processor
- Logic Circuit
	- Sequential and Combinational logic controlled by a FSM
	- n bit general purpose register
	- Has an ALU
	- External Interface (e.g. memory, I/O devices, address, control, data)
#### Simplified Processor Example
- 8 bit bus, 4 8 bit registers, tristate buffer (used to disconnect input from output)
- registers hold value to be used in computation or they hold computation results
- Control FSM: produces all logic (inputs w and a function, outputs the inputs and outputs for registers, exit status, and all other outputs)
