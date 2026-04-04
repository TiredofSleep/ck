open_hw_manager
connect_hw_server -allow_non_jtag
after 3000
set targets [get_hw_targets]
puts "Available targets: $targets"
foreach t $targets {
    puts "  TARGET: $t"
}
close_hw_manager
