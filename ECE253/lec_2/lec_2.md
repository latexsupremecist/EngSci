## Lecture 2

#### Why is hardware faster than software?
- Software usually has lots of things getting in the way
	1. Set of instructions to be excecuted
	2. Fetches instructions and data from memory
	3. Puts answers back in memory
	4. Keeps asking for instructions
	5. Very general
- Hardware has less
	1. Doesn't require instructions
	2. Data arranged to be there on time; no fetching
	3. If it isn't fast enough: build more hardware!

#### Transistors, Gates, Adders take time
- Electricity travels at the speed of light, but
- Wires have resistance
- Wires and transistors have capacitance

#### When to build hardware?
- Software are easier to create and test
- Hardware has to be manufactured, and cannot be easily modified
- It is only done when software isn't fast enough, or power is too high

#### What is assembly language?
High level languages such as C/C++ are independent of processors. A compiler such as gcc optimises it, writes architecture specific assembly which is then converted to machine code

- Assembly is only really used when high speed or specific behaviour is needed, or when making drivers for certain I/O devices
- We learn it to learn how computers operate, understand compilers and computer architecture
- We will use RISC-V in this course
	- RISC: reduced instruction-set computer
	- Open-source instruction set architecture (ISA)

#### Number systems

Decimal, Binary, Hexadecimal, 60, 20, 12
