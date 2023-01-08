# set the working dir, where all compiled verilog goes
vlib work

# compile all system verilog modules in mux.sv to working dir
# could also have multiple verilog files
vlog part2.sv

#load simulation using mux as the top level simulation module
vsim part2

#log all signals and add some signals to waveform window
log {/*}
# add wave {/*} would add all items in top level simulation module
add wave {/*}

force {ClockIn} 0
force {Reset} 1
force {Speed[1]} 0
force {Speed[0]} 1
run 1000000000ns

force {ClockIn} 1
run 1000000000ns
force {ClockIn} 0
force {Reset} 0
run 1000000000ns

force {ClockIn} 1
run 1000000000ns

force {ClockIn} 0
run 1000000000ns

force {ClockIn} 1
run 1000000000ns

force {ClockIn} 0
run 1000000000ns

force {ClockIn} 1
run 1000000000ns

force {ClockIn} 0
run 1000000000ns