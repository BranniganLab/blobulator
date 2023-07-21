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

proc assignVals {values residues mol field {seltext ""}} {
	if {$seltext ne ""} {
		set seltext "and $seltext"
	}
	set idx 0
	set last [lindex $residues 0]
	foreach id $residues {
		set step [expr $id - $last]
		if {$step>1} {
			puts "WARNING: apparent gap detected between residues $last and $id. Skipping $step blobulated residues."
			set idx [expr $idx + $step]
		}
		set selection "residue $id $seltext"
		set res [atomselect $mol $selection]
		set val [lindex $values $idx]
		$res set $field $val
		$res delete
		incr idx
		set last $id
	}
}

proc range {from to} {
	if {$to>$from} {concat [range $from [incr to -1]] $to}
}

proc dict_getwithdefault {D args} {
	if {[dict exists $D {*}[lrange $args 0 end-1]]} then {
		dict get $D {*}[lrange $args 0 end-1]
	} else {
		lindex $args end
	}
}

proc get_sequence {atomsel} {
	set seqMap [dict create GLY G ALA A VAL V PHE F PRO P MET M ILE I LEU L ASP D GLU E LYS K ARG R SER S THR T TYR Y HIS H CYS C ASN N GLN Q TRP W]

	set resids [lsort -unique [$atomsel get resid]]
	set molid [$atomsel molid]
	set chainid [lsort -unique [$atomsel get chain]]
	set cleanSelection [atomselect $molid "chain $chainid and name CA and resid $resids"]
	set resnames [$cleanSelection get resname]
	set sequence [lmap resname $resnames {dict_getwithdefault $seqMap $resname "X"}]

	return [string map {" " ""} $sequence]
}

proc get_blobs {fname atomsel} {
	set seqCol 1
	set blobCol 8
	set indexCol 9
	set blobMap [dict create h 1 p 2 s 3 "" ""]

	set blobData [readBlobulationCSV $fname]
	set blobs [readColumn $blobData $blobCol]

	puts "The blobs in this protein are: $blobs"
	puts "There are [expr [llength $blobs]] residues in this blobulation."

	set blobSeq [string map {" " ""} [readColumn $blobData $seqCol]]
	set pdbSeq [get_sequence $atomsel]

	if {$blobSeq ne $pdbSeq} {
		puts "WARNING: the sequence that was blobulated appears different from the sequence of the provided selection!"
		puts "Blobulated sequence: $blobSeq"
		puts "Selection sequence: $pdbSeq"
	}

	set userVals [lmap blb $blobs {dict get $blobMap $blb}]
	puts "User values will be $userVals"
	set residues [lsort -unique [$atomsel get residue]]
	assignVals $userVals $residues [$atomsel molid] user 

	set blobIdcs [readColumn $blobData $indexCol]
	set numericalIdcs [lmap idx $blobIdcs {regexp -all -inline -- {[0-9]+} $idx}]
	puts "Assigning user2 values: $numericalIdcs"
	assignVals $numericalIdcs $residues [$atomsel molid] user2 
}
