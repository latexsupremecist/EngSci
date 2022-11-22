## Lecture 29


### I/O
- Connecting devices to a CPU
	- memory is justa device
	- CPU communicates with it
- Memory responds to certain addresses, usually not all
- CPU can talk with other devices
	- using same method: `lw`, `sw`
	- Devices respond to certain addresses
- Memory-mapped I/O
	- Device sits on memory bus, watches for certain addresses and responds like memory for those addresses
	- Memory map of which devices respond to which addresses

#### Examples
- Suppose I/O Device 1 is assigned to memory address 0x20001000. Write code writing the value 7 to Device 1 then reading the output value from it.
```asm
li s1, 0x20001000
addi s0, zero, 7
s2 s0, 0(s1)
lw s2, 0(s1) # reads data back from device
```
- Delay loop followed by incrementing a counter on the hex display, input only
```asm
.global _start
_start:
	li s2, 0xffff0010
	mv s0, zero # pseudo instruction, same as addi s0, zero, 0
	mv s3, zero
	mv s4, zero
	mv a0, s0
	jal HEX_DECODE
	mv s3, a0
	DELAY: li s6, 50000
	LOOP: addi s6, s6, -1
	bnez s6, LOOP
	mv a0, s0
	jal HEX_DECODE
	sb s3, 1(s2)
	sb a0, (s2)
	addi s0, s0, 1
	li s8, 10
	bne s0, s8, DELAY
	addi s4, s4, 1
	bne s4, s8, UPDATE
	mv s4, zero
	UPDATE: mv a0, s4
	jal HEX_DECODE
	mv s3, a0
	mv s0, zero
	j DELAY
	END: ebreak
	HEX_DECODE:
	bnez a0, CHECK_1
	li a0, 0x3F #0b0111111
	j DONE
	CHECK_1:
		li t0, 1
		bne a0, t0, CHECK_2
		li a0, 0x06 #0b0000110
		j DONE
	CHECK_2:
		li t0, 2
		bne a0, t0, CHECK_3
		li a0, 0x5B #0b1011011
		j DONE
	CHECK_3:
		li t0, 3
		bne a0, t0, CHECK_4
		li a0, 0x4F #0b1001111
		j DONE
	CHECK_4:
		li t0, 4
		bne a0, t0, CHECK_5
		li a0, 0x66 #0b1100110
		j DONE
	CHECK_5:
		li t0, 5
		bne a0, t0, CHECK_6
		li a0, 0x6D #0b1101101
		j DONE
	CHECK_6:
		li t0, 6
		bne a0, t0, CHECK_7
		li a0, 0x7D #0b1111101
		j DONE
	CHECK_7:
		li t0, 7
		bne a0, t0, CHECK_8
		li a0, 0x07 #0b0000111
		j DONE
	CHECK_8:
		li t0, 8
		bne a0, t0, CHECK_9
		li a0, 0x7F #0b1111111
		j DONE
	CHECK_9:
		li t0, 9
		bne a0, t0, DONE
		li a0, 0x6F #0b1101111
	DONE: jr ra
```

