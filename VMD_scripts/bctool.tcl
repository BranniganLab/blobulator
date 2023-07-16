# bctool.tcl
#
# Abstract
# This file contains the functions necessary to read,
# parse, and visualize blobulation data.
# For more information about blobulation, see:
# https://www.blobulator.branniganlab.org/
# Or the GitHub repository:
# https://github.com/BranniganLab/blobulator
#
# Copyright Grace Brannigan, Rutgers University Camden

proc readBlobulationCSV {fname} {
	set file [open $fname r]
	set fileData [read $file]
	set data [split $fileData "\n"]
	close $file

	return $data
}

proc readColumn {data colIdx} {
	set column {}
	foreach row $data {
		set rowList [split $row ","]
		set value [lindex $rowList $colIdx]
		lappend column $value
	}
	set column [lreplace $column 0 0]
	return $column
}

proc assignVals {values resids mol field} {
	foreach id $resids {
		set res [atomselect top "resid $id"]
		set val [lindex $values $id]
		$res set $field $val
		$res delete
	}
}

set fname "blobs.csv"
set blobCol 8
set blobData [readBlobulationCSV $fname]
set blobs [readColumn $blobData $blobCol]

puts "The blobs in this protein are: $blobs"
puts "There are [expr [llength $blobs]] residues in this protein!"

set blobMap [dict create h 1 p 2 s 3 "" ""]
set userVals [lmap blb $blobs {dict get $blobMap $blb}]
puts "User values will be $userVals"

set protein [atomselect top protein]
set resids [lsort -unique [$protein get resid]]
assignVals $userVals $resids top user


set indexCol 9
set blobIdcs [readColumn $blobData $indexCol]
set numericalIdcs [lmap idx $blobIdcs {regexp -all -inline -- {[0-9]+} $idx}]
puts "Assigning user2 values: $numericalIdcs"
assignVals $numericalIdcs $resids top user2