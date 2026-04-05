set bit_file [file normalize [file join [file dirname [file normalize [info script]]] "ck_gen12.bit"]]
puts "Bitstream: $bit_file  ([file size $bit_file] bytes)"
open_hw_manager
connect_hw_server -allow_non_jtag
after 1000
refresh_hw_server
after 1000
set targets [get_hw_targets]
puts "Targets: $targets"
open_hw_target [lindex $targets 0]
set dev [get_hw_devices xc7z020_1]
puts "Device: $dev"
current_hw_device $dev
set_property PROGRAM.FILE $bit_file $dev
program_hw_devices $dev
puts "Gen12 programmed. T* = 5/7 is in silicon."
close_hw_target
disconnect_hw_server
close_hw_manager
