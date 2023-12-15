# bctool.tcl
#
# Abstract
# This file contains the functions necessary to read,
# parse, and visualize blobulation data.
#
# To use:
# Load your protein of choice into a vmd session and open the tkconsole
# Source this file using:
#	source /path/to/bctool.tcl
# Get the protein sequence using:
# 	set protSel [atomselect top "protein"]
#	getSequence $protSel
# Copy and paste the sequence into the blobulator and blobulate according to your needs
# Download the data using the "Download Data" button on the website
# Copy the data to your working directory
# Import the blobulation data using:
#	getBlobs my_blobulation.csv $protSel
# Visualize according to your needs. 
# User will contain 1=hydrophobic blob, 2=polar blob, 3=short blob
# User2 will contain the blob id number
#
# For more information about blobulation, see:
# https://www.blobulator.branniganlab.org/
# Or the GitHub repository:
# https://github.com/BranniganLab/blobulator
#
# Copyright Grace Brannigan, Rutgers University Camden

# readBlobulationCSV
#
# Read a csv that was written by the blobulator
#
# Arguments: 
#	a file name (string)
# Results: 
#	Opens, reads, and splits the csv into lines. The lines are returned as a single object.
proc readBlobulationCSV {fname} {
	set file [open $fname r]
	set fileData [read $file]
	set data [split $fileData "\n"]
	close $file

	return $data
}

# readColumn
#
# Extract the colIdx from the data.
#
# Arguments:
#	data: a list of lines of comma-separated data
#	colIdx: the index of the column to be extracted (zero base)
# Results:
#	Returns a list containing the values of the colIdx'th column.
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

# assignVals
# 
# Assign a list of values to the appropriate residues
#
# Arguments:
#	values: a list of values to be assigned
#	residues: the list of residue numbers to which the values will be assigned
#	mol: the molid of the residues
#	field: which field should be assigned (e.g. user or beta)
#	seltext: [optional] additional refinements to the selection text
# Results:
#	The field of the mol's residues should contain the appropriate values. 
#	If the residues are not sequential, the gap is skipped in the values list.
#	WARNING: the heuristic may not always work. If you get a warning message about a gap detected, 
#	be sure to manually check the residues before and after the indicated gap.
proc assignVals {blobSeq values residues mol field {seltext ""}} {
	if {$seltext ne ""} {
		set seltext "and $seltext"
	}
	set blbidx 0
	set blblast 0
	
	# Iterate over the residues in the structure
	foreach residue $residues {
		set selection "residue $residue $seltext"
		set res [atomselect $mol $selection]
		set resSeq [getSequence $res]
		
		# Make sure the sequences match. If not, increment.
		if {$resSeq ne [string index $blobSeq $blbidx]} {
			incr blbidx
		}	
			
		set val [lindex $values $blbidx]
		if {[catch {$res set $field $val} err]} {
		   puts "Error info $err\nFull info: $::errorInfo"
		   puts "You may have more residues in the selection than in the blobulation."
		}
		
		$res delete
		set delta [expr "$blbidx-$blblast-1"]
		if {$delta > 0} {
			puts "Warning: skipping $delta residues from the blobulation."
		}
		set blblast $blbidx
		incr blbidx
	}
}

# range
#
# Generate a list of integers from 'from' to 'to' exclusive. By Richard Suchenwirth
#
# Arguments:
#	from: the integer to start at
#	to: the integer to end at (exclusive)
# Results:
#	Return a list of integers [from, to)
proc range {from to} {
	if {$to>$from} {concat [range $from [incr to -1]] $to}
}

# dictGetWithDefault
#
# Get the corresponding value to a key or a default value if missing. By Lars Hellström
#
# Arguments:
#	D: the dict
#	args: the keys. The last value is the default value.
# Results:
#	Returns the values for keys or default if missing
proc dictGetWithDefault {D args} {
	if {[dict exists $D {*}[lrange $args 0 end-1]]} then {
		dict get $D {*}[lrange $args 0 end-1]
	} else {
		lindex $args end
	}
}

# getSequence
#
# Get the one-letter sequence of an atomselection. Use X if the residue isn't recognized.
#
# Arguments:
#	atomsel: an atomselection
# Results:
#	Return the one-letter sequence of the atomselection as a string. Unrecognized residues will be transcribed as X.
proc getSequence {atomsel} {
	set seqMap [dict create GLY G ALA A VAL V PHE F PRO P MET M ILE I LEU L ASP D GLU E LYS K ARG R SER S THR T TYR Y HIS H CYS C ASN N GLN Q TRP W]

	set residues [lsort -unique [$atomsel get residue]]
	set molid [$atomsel molid]
	set chainid [lsort -unique [$atomsel get chain]]
	set cleanSelection [atomselect $molid "chain $chainid and name CA and residue $residues"]
	set resnames [$cleanSelection get resname]
	set sequence [lmap resname $resnames {dictGetWithDefault $seqMap $resname "X"}]

	return [string map {" " ""} $sequence]
}

# getBlobs
#
# Read and assign blob identities from a csv file (generated by the blobulator) to an atomselection
# User contains 1=h, 2=p, 3=s
# User2 contains the blob id
#
# Arguments:
# 	fname: the name of the csv file
#	atomsel: an atomselection that corresponds to the sequence in the blobulation
# Results:
#	Blob types get saved to the user field (h=1, p=2, s=3) blob indices get saved to user2
proc getBlobs {fname atomsel} {
	set seqCol 1
	set blobCol 8
	set indexCol 9
	set blobMap [dict create h 1 p 2 s 3 "" ""]

	set blobData [readBlobulationCSV $fname]
	set blobs [readColumn $blobData $blobCol]

	puts "The blobs in this protein are: $blobs"
	puts "There are [expr [llength $blobs]] residues in this blobulation."

	set blobSeq [string map {" " "" "{" "" "}" ""} [readColumn $blobData $seqCol]]
	set pdbSeq [getSequence $atomsel]
	
	if {$blobSeq ne $pdbSeq} {
		puts "WARNING: the sequence that was blobulated appears different from the sequence of the provided selection!"
		puts "Blobulated sequence: $blobSeq"
		puts "Selection sequence: $pdbSeq"
	}

	set userVals [lmap blb $blobs {dict get $blobMap $blb}]
	puts "User values will be $userVals"
	set residues [lsort -unique -integer [$atomsel get residue]]

	assignVals $blobSeq $userVals $residues [$atomsel molid] user

	set blobIdcs [readColumn $blobData $indexCol]
	set numericalIdcs [lmap idx $blobIdcs {regexp -all -inline -- {[0-9]+} $idx}]
	puts "Assigning user2 values: $numericalIdcs"
	assignVals $blobSeq $numericalIdcs $residues [$atomsel molid] user2 
}
