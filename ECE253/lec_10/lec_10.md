## Lecture 10

### 3-variable K-map
Gray code: only one bit has changed between any 2 consecutive binary representations

|$x_3$\\$x_1x_2$ | 00 | 01 | 11 | 10 |
| --- | --- | --- | --- | --- |
| 0 | $m_0$ | $m_2$ | $m_6$ | $m_4$ |
| 1 | $m_1$ | $m_3$ | $m_7$ | $m_5$ |

To find $x_2x_3$, we can refer to the K-map, which gives us $m_3$ and $m_7$, which can then be simplified as
$$x_2x_3 = \overline{x_1}x_2x_3 + x_1x_2x_3 = x_2x_3(\overline{x_1} + x_1) = x_2x_3$$
If we want $m_2+m_6$, we can see directly from the map that it corresponds to $x_2\overline{x_3}$. Similarly, $m_2+m_3+m_6+m_7=x_2$.

#### Example

| z\\xy | 00 | 01 | 11 | 10 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 |

$f$ is equal to 1 on the first row and column, so
$$f = \overline{xy} + \overline{z}$$

### Terminology
- Implicant: for a function f, an implicant is any product term in f
	- e.g. $m_0$, $m_1$, etc
- Prime Implicant: an implicant for which is it not possible to remove any literal and still have a valid implicant
	- e.g. $\overline{z}$ in the above example is a prime implicant, but $\overline{xz}$ is not ($\overline{x}$ can be removed)
- Cover: any set of implicants that include all minterms of a function. Consider
|$x_3$\\$x_1x_2$ | 00 | 01 | 11 | 10 |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 | 1 |
All prime implicants are $x_1\overline{x_3}, x_1\overline{x_2}, \overline{x_2}x_3$. The **minimum** cost cover, however, is
$$f = x_1\overline{x_3} + \overline{x_2}x_3$$
- Essential prime implicant: prime implicant that covers at least one minterm not covered by any other prime implicant
	- In the above example, they are $x_1\overline{x_3}$, $\overline{x_2}x_3$

### 4-variable K-maps
*Note that anything beyond is difficult in 2D*

| $x_3x_4$\\$x_1x_2$ | 00 | 01 | 11 | 10 |
| --- | --- | --- | --- | --- |
| 00 | $m_0$ | $m_4$ | $m_{12}$ | $m_8$ |
| 01 | $m_1$ | $m_5$ | $m_{13}$ | $m_9$ |
| 11 | $m_3$ | $m_7$ | $m_{15}$ | $m_{11}$ |
| 10 | $m_2$ | $m_6$ | $m_{14}$ | $m_{10}$ |

The first two rows are $\overline{x_3}$.  
The four cells in the middle are $x_2x_4$.

#### Example $$f(x_1,x_2,x_3,x_4) = \sum m(2,4,5,8,10,11,12,13,15)$$

| $x_3x_4$\\$x_1x_2$ | 00 | 01 | 11 | 10 |
| --- | --- | --- | --- | --- |
| 00 | 0 | 1 | 1 | 1 |
| 01 | 0 | 1 | 1 | 0 |
| 11 | 0 | 0 | 1 | 1 |
| 10 | 1 | 0 | 0 | 1 |

The prime implicants are $x_2\overline{x_3}, x_1\overline{x_3x_4}, x_1x_2x_4, x_1x_3x_4, x_1\overline{x_2}x_3, \overline{x_2}x_3\overline{x_4}, x_1\overline{x_2x_4}$  
The essential prime implicants are $x_2\overline{x_3}, \overline{x_2}x_3\overline{x_4}$  
The minimum cost cover is
$$f = x_2\overline{x_3} + \overline{x_2}x_3\overline{x_4} + x_1x_3x_4 + x_1\overline{x_2x_4}$$
There can be more than one minimum cost covers (the last term can be replaced by $x_2\overline{x_3x_4}$
