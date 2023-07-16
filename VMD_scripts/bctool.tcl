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

	return $column
}

set fname "blobs.csv"
set blobCol 8
set blobData [readBlobulationCSV $fname]
set blobs [readColumn $blobData $blobCol]

puts "The blobs in this protein are: $blobs"
puts "There are [expr [llength $blobs]] residues in this protein!"

set blobMap [dict create h 0 p 1 s 2 "" ""]
set userVals [lmap blb $blobs {dict get $blobMap $blb}]
puts "User values will be $userVals"


set protein [atomselect top protein]
set resids [lsort -unique [$protein get resid]]
foreach id $resids {
	set res [atomselect top "resid $id"]
	set val [lindex $userVals $id]
	$res set user $val
	$res delete
}
#----------SHOW BLOB INDEX NUMBER---------
set j 1
foreach {row} $datarow {
	set listofElements2 [list [lindex $datarow $j]]
	set datacol2 [split $listofElements2 ","]
	set onlyIndex7 [lindex $datacol2 7]
	lappend col7 $onlyIndex7
	incr j
	unset listofElements2
	unset onlyIndex7
	unset datacol2
}

puts "The blob index numbers are: $col7"
unset col7

#-----------COLOR BY BLOB INDEX------------
set a 0
set b 1
set c 3
set d 4
set k 0

foreach {blobtype} $newcol6 {
	set blobBefore [lindex $newcol6 $a]
	set blobAfter [lindex $newcol6 $b]
	if {$blobAfter==$blobBefore} {
		set sel [atomselect top "resid $a"]
		$sel set user2 $k
		puts "Coloring same index..."
		$sel delete
	}  else  {
		set sel [atomselect top "resid $a"]
		$sel set user2 $k
		puts "Coloring new index..."
		$sel delete
		incr k
	}
	incr a
	incr b
	mol modcolor 0 0 User2		;# USER CHANGES MOL ID HERE ***
}

#UNSET COL6 AND NEWCOL6 IF YOU WISH TO RUN SCRIPT AGAIN
unset col6
unset newcol6

close $file