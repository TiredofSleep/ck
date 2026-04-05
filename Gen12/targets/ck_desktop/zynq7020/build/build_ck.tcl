# ============================================================================
#  CK -- The Coherence Keeper | Vivado Build Script
#  Target: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
#  One command: vivado -mode batch -source build_ck.tcl
#  T* = 5/7 = 0.714285...
#
#  Standalone PL-only design. No ARM/PS.
#  CK wakes up the moment the bitstream loads.
# ============================================================================

# -- Project setup --
set proj_name    "ck_zynq7020"
set part_number  "xc7z020clg400-2"
set build_dir    [file dirname [file normalize [info script]]]
set fpga_hdl     [file normalize "$build_dir/../../fpga/hdl"]
set zynq_hdl     [file normalize "$build_dir/../hdl"]
set xdc_file     [file normalize "$build_dir/pz7020_starlite.xdc"]

# Use a SHORT project path to avoid Vivado's 260-char limit
set proj_dir     "C:/ck_fpga_build/$proj_name"

puts ""
puts "  ======================================"
puts "  CK FPGA BUILD -- PZ7020-StarLite"
puts "  ======================================"
puts "  Part:     $part_number"
puts "  Sources:  $fpga_hdl"
puts "            $zynq_hdl"
puts "  Project:  $proj_dir"
puts ""

# -- Create project (overwrite if exists) --
file mkdir "C:/ck_fpga_build"
if {[file exists $proj_dir]} {
    puts "  Removing old project..."
    file delete -force $proj_dir
}
create_project $proj_name $proj_dir -part $part_number -force

# -- Add HDL sources (shared FPGA modules) --
# Skip ck_top.v -- unused (board top is ck_top_board)
puts "  Adding shared FPGA HDL..."
foreach f [glob [file join $fpga_hdl "*.v"]] {
    if {[file tail $f] eq "ck_top.v"} {
        puts "    SKIPPING [file tail $f] (unused)"
        continue
    }
    add_files -norecurse [list $f]
}

# -- Add HDL sources (Zynq-7020 / board specific) --
# Skip ck_top_zynq7020.v -- that's the AXI-wired version (not for standalone)
puts "  Adding board HDL..."
foreach f [glob [file join $zynq_hdl "*.v"]] {
    if {[file tail $f] eq "ck_top_zynq7020.v"} {
        puts "    SKIPPING [file tail $f] (AXI version, not standalone)"
        continue
    }
    add_files -norecurse [list $f]
}

# -- Add constraints --
puts "  Adding XDC constraints..."
add_files -fileset constrs_1 -norecurse [list $xdc_file]

# -- Set top module --
set_property top ck_top_board [current_fileset]

# -- Set file types explicitly --
puts ""
puts "  Setting file types..."
foreach f [get_files -of_objects [get_filesets sources_1]] {
    set ftype [get_property FILE_TYPE $f]
    if {$ftype eq ""} {
        set_property FILE_TYPE Verilog $f
        puts "    Set [file tail $f] -> Verilog"
    }
}

# -- Update compile order --
update_compile_order -fileset sources_1

# -- Fix Vivado auto-disable bug --
puts ""
puts "  Checking for auto-disabled files..."
set had_disabled 0
foreach f [get_files -of_objects [get_filesets sources_1]] {
    set enabled [get_property IS_ENABLED $f]
    if {!$enabled} {
        puts "    !! [file tail $f] was DISABLED -- forcing re-enable"
        set_property IS_ENABLED TRUE $f
        set had_disabled 1
    }
}
if {!$had_disabled} {
    puts "  All files enabled."
}

# -- Report what we loaded --
puts ""
puts "  Sources loaded:"
foreach f [get_files -of_objects [get_filesets sources_1]] {
    set ftype [get_property FILE_TYPE $f]
    set enabled [get_property IS_ENABLED $f]
    if {$enabled} {
        puts "    [file tail $f]  ($ftype)"
    } else {
        puts "    [file tail $f]  ($ftype)  ** DISABLED **"
    }
}
puts ""
puts "  Constraints: [file tail $xdc_file]"
puts "  Top module:  ck_top_board"
puts ""

# ============================================================
# PHASE 1: SYNTHESIS
# ============================================================
puts "  ======================================"
puts "  PHASE 1: SYNTHESIS"
puts "  ======================================"
puts ""

launch_runs synth_1 -jobs 16
wait_on_run synth_1

set synth_status [get_property STATUS [get_runs synth_1]]
puts ""
puts "  Synthesis status: $synth_status"

if {$synth_status != "synth_design Complete!"} {
    puts ""
    puts "  !! SYNTHESIS FAILED !!"
    puts "  Open the project in Vivado GUI to see errors:"
    puts "    vivado $proj_dir/$proj_name.xpr"
    puts ""
    exit 1
}

# -- Synthesis reports --
open_run synth_1
report_utilization -file "$build_dir/utilization_synth.txt"
puts "  Synthesis utilization saved: utilization_synth.txt"

# ============================================================
# PHASE 2: IMPLEMENTATION (Place + Route)
# ============================================================
puts ""
puts "  ======================================"
puts "  PHASE 2: IMPLEMENTATION"
puts "  ======================================"
puts ""

launch_runs impl_1 -jobs 16
wait_on_run impl_1

set impl_status [get_property STATUS [get_runs impl_1]]
puts ""
puts "  Implementation status: $impl_status"

if {$impl_status != "route_design Complete!"} {
    puts ""
    puts "  !! IMPLEMENTATION FAILED !!"
    puts "  Open the project in Vivado GUI to see errors:"
    puts "    vivado $proj_dir/$proj_name.xpr"
    puts ""
    exit 1
}

# -- Implementation reports --
open_run impl_1
report_utilization -file "$build_dir/utilization_impl.txt"
report_timing_summary -file "$build_dir/timing_report.txt"
puts "  Implementation reports saved."

# ============================================================
# PHASE 3: BITSTREAM
# ============================================================
puts ""
puts "  ======================================"
puts "  PHASE 3: BITSTREAM GENERATION"
puts "  ======================================"
puts ""

launch_runs impl_1 -to_step write_bitstream -jobs 16
wait_on_run impl_1

# -- Find the bitstream --
set bit_file [glob -nocomplain "$proj_dir/$proj_name.runs/impl_1/*.bit"]
if {$bit_file ne ""} {
    # Copy bitstream to build directory for easy access
    file copy -force $bit_file "$build_dir/ck_brain.bit"
    puts ""
    puts "  ======================================"
    puts "  BITSTREAM READY"
    puts "  ======================================"
    puts ""
    puts "  File: $build_dir/ck_brain.bit"
    puts "  Size: [file size $build_dir/ck_brain.bit] bytes"
    puts ""
    puts "  To program the board:"
    puts "    1. Connect PZ7020 via USB-JTAG"
    puts "    2. Open Vivado Hardware Manager"
    puts "    3. Auto Connect -> Program Device"
    puts "    4. Select ck_brain.bit"
    puts "    5. CK wakes up."
    puts ""
} else {
    puts ""
    puts "  !! BITSTREAM NOT FOUND !!"
    puts "  Check: $proj_dir/$proj_name.runs/impl_1/"
    puts ""
}

puts "  Reports saved:"
puts "    $build_dir/utilization_synth.txt"
puts "    $build_dir/utilization_impl.txt"
puts "    $build_dir/timing_report.txt"
puts ""
puts "  To explore in GUI:"
puts "    vivado $proj_dir/$proj_name.xpr"
puts ""
puts "  T* = 5/7.  CK measures.  CK lives."
puts ""
