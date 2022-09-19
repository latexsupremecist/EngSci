## Lecture 2

#### Crystal Structure vs Crystal Lattice
- Structure: physical
- Lattice: mathematical
    - Primitive: one **lattice point** per cell (not atom)

#### Wigner-Seitz Cell
- Draw a line from each lattice point to its nearest neighbour
- The perpendicular bisectors of each line form a Wigner-Seitz Cell
- The 3-D case is analogous

#### Reciprocal Lattice in 2-D
- Let the original lattice vectors be $\textbf{a}, \textbf{b}$ with lengths $\alpha, \beta$ respectively
- The basis vectors in the reciprocal lattice $\textbf{a*}, \textbf{b*}$ are then perpendicular to $\textbf{b}, \textbf{a}$ and have lengths $\frac{1}{\alpha}, \frac{1}{\beta}$ respectively
- The 3-D case is analogous
- To be more exact, $\textbf{a*}$ is in the direction perpendicular to the (100) plane with magintude the inverse of the $d_{100}$ (distance between origin and the (100) plane)

#### Brillouin zone in 2-D
- The first Brillouin zone in a reciprical lattice is constructed exactly the same as how Wigner-Seitz cells are constructed in a real lattice

#### Equivalent cells in 3-D
- Similar to the 2-D case, the same cells can be named differently. Usually, cubic fcc is preferred as it is a special rhombohedral case with $\frac{\pi}{3}$ radians

#### Miller Indices
1. Select origin not in contact with lattice plane and define basis vectors
2. Determine intercepts of lattice plane with basis vectors
3. Take reciprocals of intercepts
4. Remove fractions but do not reduce index values using lowest common factor
5. Negative index values are represented with $\overline{x}$
6. A lattice plane and its negative are equivalent
7. Round brackets () for specific lattice planes
8. Brace brackets {} for family of lattice planes, order, sign does not matter
    - e.g. $(111)$ and $(\overline{1}\overline{1}\overline{1})$ are in $\{111\}$, but not $(\overline{1}11)$

#### Miller - Bravais Indices
- Miller Indices: (hkl)
- Miller-Bravais Indices: (hkil), where $h + k + i = 0$ or $i = -(h+k)$
- Planes with similar Miller-Bravais Indices are identical, but their Miller Indices may be different 

#### Directions in Hexagonal Lattice
- Directions in general are written in the form of \[abc\] (or \<abc\> for general directions)
- They are also written in 4 (redundant) Weber indices

\[uvw\] $\rightarrow$ \[u'v'tw'\]
\begin{align*} u' &= \frac{n(2u-v)}{3} \\ v' &= \frac{n(2v-u)}{3} \\ t &= -(u+v) \\ w' &= nw \\ \end{align*}
Where $n$ is a factor that could be used to make new indices into smallest integers

\[u'v't'w'\] $\rightarrow$ \[uvw\]
\begin{align*} u &= u' - t' \\ v &= v' - t' \\ w &= w' \\ \end{align*}

#### Equations:
- A direction lies on a plane if $$uh + vk + wl = 0$$
- The intersection of two planes is the direction where
\begin{align*} u &= k_1l_2 - k_2l_1 \\ v &= h_2l_1 - h_1l_2 \\ w &= h_1k_2 - h_2k_1 \\ \end{align*}