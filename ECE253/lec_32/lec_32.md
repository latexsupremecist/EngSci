## Lecture 32

### Timing Analysis
- Increase in clock speed has been the major boost of performance for many years
- But physical delays in the circuit pose a limit to maximum clock speed
- Setup Time: t<sub>su</sub>, the data D must be stable during the setup time to ensure it correctly feeds into flip flop upon rising clock edge
- Hold Time: t<sub>h</sub> Data must remain stable for the hold time
$$T_\mathrm{min} = \sum t_i \Rightarrow F_\mathrm{max} = \frac{1}{T_\mathrm{min}}$$
- Clock skew: possible for clock edge to not arrive at the same time at all flip flops
	- Clock source and clock sink arrive at different times, and the skew is their difference
	- Flip Flop of sink has input depending on output of source
	- Positive skew: more time, higher fmax
	- Negative skew: opposite

### Calculations
- Calculate clock: look for longest path, including setup time
- Calculate hold time violation: shortest path
	- data racing the clock; setup time not used
$$t_h + \Delta \leq t_{CQ} + t_\mathrm{logic_main}$$
- Setup time violation: logic is too slow for correct value to arrive at input to FF before t<sub>su</sub> before clock edge
$$t_\mathrm{min} \geq t_{CQ} + t_\mathrm{logic_max} + t_{su} + \Delta_1$$

