vlib work

# compile all system verilog modules in mux.sv to working dir
# could also have multiple verilog files
vlog part3.sv

#load simulation using mux as the top level simulation module
vsim part3

#log all signals and add some signals to waveform window
log {/*}
# add wave {/*} would add all items in top level simulation module
add wave {/*}

force {ClockIn} 0
force {Reset} 1
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
force {Reset} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
force {Start} 1
force {Letter[2]} 0
force {Letter[1]} 0
force {Letter[0]} 0
run 250000000ns

force {ClockIn} 0
force {Start} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns

force {ClockIn} 1
run 250000000ns

force {ClockIn} 0
run 250000000ns