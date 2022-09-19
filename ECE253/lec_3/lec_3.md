## Lecture 3

#### Binary
- For $n$ binary digits, we can represent $2^n$ values
- Binary to Decimal:
	- Add up the powers of 2, e.g. $(1111)_2 = 2^3 + 2^2 + 2^1 + 2^0 = (15)_{10}$
- Decimal to Binary:
	- Divide the number by 2, and the remainder is the rightmost digit
	- e.g. 11/2 = 5R1, 5/2 = 2R1, 2/2 = 1R0, 1/2 = 1R1, so $(11)_{10} = (1011)_2$ (reading the remainders from right to left)

#### Hexadecimal:
- Hexadecimal to Binary:
	- Add up the powers of 16, similar to binary
- Decimal to Hexadecimal:
	- Either divide the number by 16 and keep the remainder as the rightmost digit (as in binary)
	- Or convert it to binary then conver every 4 binary digits to a hexadecimal digit (from the right)

#### Miscellaneous:
- Negative numbers will be covered later in the term
- Fractions: Either fixed point of floating point
	- Floating point: a number is represented as $1.100110... \times 2^{101...}$, i.e. two signed binary numbers

#### Addition of binary numbers
- Exactly the same as decimal, but carry over happens at 2 instead of 10

#### Addition of hexadecimal numbers
- Exactly the same as decimal, but carry over happens at 16 instead of 10 *(note than the numbers 10-15 become A-F, they do not carry over!)*

#### Transistors as switches
- Transistors are the key technology to enable modern computers
- Moore's Laws: number of transistors manufactured on a chip doubles every 1.5 - 2 years
- Transistors operate as switches **in this class**
	- $x = 0$: Light is off
	- $x = 1$: Light is on
- Two or more transistors:
	- Series: AND
	- Parallel: OR
- NOT function: transistor and light bulb connected in parallel between voltage and ground
