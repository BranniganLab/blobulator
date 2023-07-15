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

proc readColumn {data, colIdx} {
	set column {}
	foreach row $data {
		set rowList [split $row ","]
		set value [lindex $datacol $colIdx]
		lappend column $value
	}

	return $column
}

set fname "blobs.csv"
set blobCol 9
set blobData [readBlobulationCSV $fname]
set blobs [readColumn $blobData $blobCol]



puts "The blobs in this protein are: $blobs"
puts "There are [expr [llength $blobs] -1] residues in this protein!"

#---------COLOR BY BLOB TYPE-----------
#set HTYPE 0 ---> these create an error in the code
#set PTYPE 1
#set STYPE 2

set newcol6 [linsert $col6 0 0]
set i 1
foreach {blob} $newcol6 {
	set checkBlob [lindex $newcol6 $i]
	if {$checkBlob=="h"} {
		set sel [atomselect top "resid $i"]
		$sel set user 0
		puts "resid $i is a h blob"
		$sel delete
	}

	if {$checkBlob=="p"} {
		set sel [atomselect top "resid $i"]
		$sel set user 1
		puts "resid $i is an p blob"
		$sel delete
	}

	if {$checkBlob=="s"} {
		set sel [atomselect top "resid $i"]
		$sel set user 2
		puts "resid $i is an s blob"
		$sel delete
	}
	incr i
}
mol modcolor 0 0 User		;# USER CHANGES MOL ID HERE ***


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