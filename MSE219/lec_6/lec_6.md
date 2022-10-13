## Lecture 6

### Tensors
- A collection of properties that do not depend on a basis
- Example:
$$\begin{bmatrix} J_1 \\ J_2 \\ J_3 \end{bmatrix} = \begin{bmatrix} \sigma_{11} & \sigma_{12} & \sigma_{13} \\ \sigma_{21} & \sigma_{22} & \sigma_{23} \\ \sigma_{31} & \sigma_{32} & \sigma_{33} \end{bmatrix} \begin{bmatrix} E_1 \\ E_2 \\ E_3 \end{bmatrix}$$
which can be written more compactly as
$$J_1 = \sigma_{ij}E_j$$
where the rank is equal to the number of subscripts. The principal components are the diagonal elements $\sigma_{ii}$.

### Anisotropic case
E is along the $x$ axis, so
\begin{align*}
J_1 &= \sigma_{11}E_1 \\
J_2 &= \sigma_{21}E_2 \\
J_3 &= \sigma_{31}E_3
\end{align*}
where $J_1$ is the principal component, and the rest are transverse components.

#### Einstein Convention
If the same dummy variable appears more than once, a summation is implied

### Transformation of Axes
From Cartesian Coordinates, the transformation (rotation) matrix is given by $A = [a_{ij}]$ where $a_{ij}$ denotes the angle between the new axis $x_i'$ and the old axis $x_j$.

#### Example
Our original equation is
$$J_p = \sigma_{pq}E_q$$
Combining this with transformation of axes
$$J_i' = a_{ip}J_p$$
we have
$$J_i' = a_{ip}\sigma_{pq}E_q$$

### Tensor Property Transformation Law
$$\sigma_{ij}' = a_{ip}a_{jq}\sigma_{pq}'$$
$$T_{ij}' = a_{ip}a_{jq}T_{pq}'$$
Note: $m$ rank tensor related to $n$ rank tensor by $(m+n)$ rank tensor.

### Third Rank Tensors
- Piezoelectricity: stress produces electric dipole moment
- Isotropic case: $D = d\sigma$, where d is the piezoelectric modulus
- Anisotripic case: $D_i = d_{ijk}\sigma_{jk}$
- Normal stresses: $s_{ii}$
- Transverse (shear) stresses: $s_{ij}, i \neq j$
- No turning moment: $\sigma_{ij} = \sigma_{ji}$

### Symmetrical Tensors (rank 2 tensors)
$$T_{ij} = T_{ji} = [S_{ij}]$$
where
$$[S_{ij}] = \begin{bmatrix} s_{11} & s_{12} & s_{13} \\ s_{12} & s_{22} & s_{23} \\ s_{13} & s_{23} & s_{33} \end{bmatrix}$$
which has only 6 independent terms.  
In fact, piezoelectric tensors are symmetric for the latter 2 terms, ie
$$d_{ijk} = d_{ikj}$$
which gives us 18 independent $d_{ijk}$ terms
