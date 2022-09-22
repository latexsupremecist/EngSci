## Lecture 6

### Boolean Identities:
$+$ and $\cdot$ are commutative, associative, and distributive

### Any SOP circuit can be implimented as NAND NAND
- Example: $f = x_1x_2 + x_2x_3$ can be rewritten as $f = (x_1 \text{ NAND } x_2) \text{ NAND } (x_2 \text{ NAND } x_3)$

### Any POS circuit can be implemented as NOR NOR
- Example: $f = (x_1+x_2)(x_2+x_3)$ can be rewritten as $f = (x_1 \text{ NOR } x_2) \text{ NOR } (x_2 \text{ NOR } x_3)$

### Design Example
Gumball factory
- $s_2$ normally gives 0, but $s_2 = 1$ if gumball is too large
- $s_1$ normally gives 0, but $s_1 = 1$ if gumball is too small
- $s_0$ normally gives 0, but $s_0 = 1$ if gumball is too light  
Synthesise a logic function $f = 1$ when a gumball is either too large, or both too small and too light
- By inspection: $s_2 + s_1s_0$
- From truth table:
\begin{align*}
f &= \overline{s_2}s_1s_0 + s_2\overline{s_1}\overline{s_0} + s_2\overline{s_1}s_0 + s_2s_1\overline{s_0} + s_2s_1s_0 \\
&= s_1s_0 + s_2\overline{s_1} + s_2\overline{s_0} \\
&= s_1s_0 + s_2(\overline{s_1} + \overline{s_0}) \\
&= s_1s_0 + s_2(\overline{s_1s_0}) \\
&= s_1s_0 + s_2 \\
\end{align*}

### Minimal POS Example
Derive a minimal POS for $f(x_1, x_2, x_3) = \prod M(0,2,4)$  
\begin{align*}
f &= (x_1 + x_2 + x_3)(x_1 + \overline{x_2} + x_3)(\overline{x_1} + x_2 + x_3) \\
&= (x_1 + x_3)(x_2 + x_3) \\
\end{align*}
Using the minterms of $\overline{f}$
\begin{align*}
\overline{f} &= \overline{x_1x_2x_3} + \overline{x_1}x_2\overline{x_3} + x_1\overline{x_2x_3} \\
&= \overline{x_1x_3} + \overline{x_2x_3} \\
\end{align*}
So $$f = \overline{\overline{f}} = \overline{(\overline{x_1x_3} + \overline{x_2x_3})} = \overline{(\overline{x_1x_3})}\overline{(\overline{x_2x_3})} = (\overline{\overline{x_1}} + \overline{\overline{x_3}})(\overline{\overline{x_2}} + \overline{\overline{x_3}}) = (x_1+x_3)(x_2+x_3)$$
