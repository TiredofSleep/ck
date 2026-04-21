set bit_file [file normalize [file join [file dirname [file normalize [info script]]] "ck_gen12.bit"]]
puts "Bitstream: $bit_file"
open_hw_manager
connect_hw_server -allow_non_jtag
after 1000
refresh_hw_server
after 2000
set targets [get_hw_targets]
puts "Targets found: $targets"
open_hw_target [lindex $targets 0]
current_hw_device [lindex [get_hw_devices] 0]
set dev [current_hw_device]
puts "Device: $dev"
set_property PROGRAM.FILE $bit_file $dev
program_hw_devices $dev
puts "Gen12 programmed. T* = 5/7 is in silicon."
close_hw_target
disconnect_hw_server
close_hw_manager
