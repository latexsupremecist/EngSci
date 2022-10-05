## Lecture 11

### Procedure for finding a minimum-cost cover
1. Find PIs
2. Include Essential PIs in the cover
3. If needed, choose other PIs (as few as possible) to cover all minterms
*Remember K-maps wrap around edges and corners*

### Don't Cares
- Either specific inputs don't occur
- Or we don't care
- Leads to cheaper logic

Consider a 4 digit binary input where we do not care about the terms A-F. Then

| $x_1x_0$\\$x_3x_2$ | 00 | 01 | 11 | 10 |
| --- | --- | --- | --- | --- |
| 00 | 0 | 1 | d | 0 |
| 01 | 1 | 0 | d | 0 |
| 11 | 0 | 0 | d | d |
| 10 | 0 | 0 | d | d |

Then we have $h_0 = \overline{x_1x_3}(\overline{x_0}+\overline{x_2})(x_0+x_2)$

### Sequential Circuits
- Combinational circuits: outputs are only determined by present inputs
- Sequential circuits: outputs are determined by both present inputs and previous inputs
- Example: Alarm System
	- R reset
	- S: sensor
	- Alarm starts once S is on, only stops when R is reset

R NOR (S NOR Q) = Q  
Note that R, S, Q all start with 0. Therefore when S is triggered, S = Q = 1, R = 0. Even when S returns to 0, Q = 1, S = R = 0. Only by resetting (R = 1) will the alarm stop. Of course, undoing the reset (R = 0) will stop the alarm if and only if S = 0.

### RS Latch
- Cross Coupled NOR gates
