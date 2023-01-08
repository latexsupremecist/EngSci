# set the working dir, where all compiled verilog goes
vlib work

# compile all system verilog modules in mux.sv to working dir
# could also have multiple verilog files
vlog part1.sv

#load simulation using mux as the top level simulation module
vsim part1

#log all signals and add some signals to waveform window
log {/*}
# add wave {/*} would add all items in top level simulation module
add wave {/*}

force {Reset} 1
force {Clock} 0
run 10ns

force {Clock} 1
run 10ns

force {Reset} 0
force {Clock} 0
force {Enable} 0
run 10ns

force {Clock} 1
force {Enable} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns