## Lecture 15

### Generate different clock from given clock
- 2 approaches
	- Using a gated D latch, $D = \overline{Q}$, which halves the frequency
	- Using a counter (attached to the clock) as D

### Finite State Machines
- Named because a circuit with k registers can have at most $2^k$ states

#### Example
- Motor outputs status w
- If status is okay, output of FSM z = 0
- if a sequence of w is 1, 0, 1, an error has occurred, outputs z = 1
- z is fed back into the circuit
- Design Step 1: State Diagram
	- State A (z = 0): a bunch of zeros
	- State B (z = 0): a bunch of zeros then a 1
	- State C (z = 0): a bunch of zeros then 1, 0
	- State D (z = 1): a bunch of zeros then 1, 0, 1
	- We can write a table

| Present State | w = 0 | w = 1 | z |
| --- | --- | --- | --- |
| A | A | B | 0 |
| B | C | B | 0 |
| C | A | D | 0 |
| D | C | B | 1 |

We need 2 flip flops (2 bits) with state codes A = 00, B = 01, C = 10, D = 11. Substituting into the table with the convention $y=$ previous output, $Y=$ next output,

| $y_2y_1$ | $Y_2Y_1$ (w = 0) | $Y_2Y_1$ (w = 1) | z |
| --- | --- | --- | --- |
| 00 | 00 | 01 | 0 |
| 01 | 10 | 01 | 0 |
| 10 | 00 | 11 | 0 |
| 11 | 10 | 01 | 1 |

By inspection, $Y_1 = w$, $z = y_2y_1$. Using a k-map, $Y_2 = \overline{w}y + wy_2\overline{y_1}$.

