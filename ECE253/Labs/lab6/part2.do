vlib work
vlog part2.sv
vsim part2
log{/*}
add wave {/*}

force {Clock} 0
force {Reset} 1
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
force {Reset} 0
force {Go} 1
force {DataIn[0]} 0
force {DataIn[1]} 0
force {DataIn[2]} 0
force {DataIn[3]} 0
force {DataIn[4]} 0
force {DataIn[5]} 0
force {DataIn[6]} 0
force {DataIn[7]} 1
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
force {Go} 0
run 10ns

force {Clock} 0
force {Go} 1
force {DataIn[0]} 0
force {DataIn[1]} 0
force {DataIn[2]} 0
force {DataIn[3]} 0
force {DataIn[4]} 0
force {DataIn[5]} 0
force {DataIn[6]} 0
force {DataIn[7]} 1
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
force {Go} 0

force {Clock} 0
force {Go} 1
force {DataIn[0]} 0
force {DataIn[1]} 0
force {DataIn[2]} 0
force {DataIn[3]} 0
force {DataIn[4]} 0
force {DataIn[5]} 0
force {DataIn[6]} 1
force {DataIn[7]} 0
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
force {Go} 0
run 10ns

force {Clock} 0
force {Go} 1
force {DataIn[0]} 0
force {DataIn[1]} 0
force {DataIn[2]} 0
force {DataIn[3]} 0
force {DataIn[4]} 0
force {DataIn[5]} 0
force {DataIn[6]} 1
force {DataIn[7]} 0
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
force {Go} 0
run 10ns

force {Clock} 0
force {Go} 1
force {DataIn[0]} 0
force {DataIn[1]} 0
force {DataIn[2]} 0
force {DataIn[3]} 0
force {DataIn[4]} 0
force {DataIn[5]} 0
force {DataIn[6]} 1
force {DataIn[7]} 1
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
force {Go} 0
run 10ns

force {Clock} 0
force {Go} 1
force {DataIn[0]} 0
force {DataIn[1]} 0
force {DataIn[2]} 0
force {DataIn[3]} 0
force {DataIn[4]} 0
force {DataIn[5]} 1
force {DataIn[6]} 0
force {DataIn[7]} 0
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

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns

force {Clock} 1
run 10ns

force {Clock} 0
run 10ns