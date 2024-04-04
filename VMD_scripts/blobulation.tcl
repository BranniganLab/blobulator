

proc blobulate {MolID lMin H} {
	#
	#	The overarching proc, users use this to run program
	#
	#
	#	Arguments:
	#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
	#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
	# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
	#	for an h blob
	#
	#	Results:
	#	The results is a user value applied to the protein of choice the differentiates h blobs, p blobs, and s blobs. 
	
	source normalized_hydropathyscales.tcl
	set checked [checker $MolID $lMin $H]
	if {$checked == -1} {
		puts "Variables are incorrect ending program"
		return  
		}
	set sequence [getSequence $MolID]
	set hydroS [hydropathyScores $KD_Normalized $sequence]
	if {$hydroS == -1} {
		return -1
		}
	set hydroM [hydropathyMean $hydroS $sequence]
	set dig [Digitize $H $hydroM ]
	set blobh [ blobH $dig $lMin ]
	set blobs [ blobS $blobh $dig $lMin ]
	set blobp [ blobP $blobs $dig ]
    	set blobulated [blobAssign $blobp]
    		
	#Makes sure procedures that fail to pass checks can't assign values. 
	if {$blobulated != -1} {
	set lower [string tolower $MolID]
	set sel [atomselect $lower alpha]
	$sel set user $blobulated
	$sel get user
	$sel delete
	} 
	return $blobulated
}

proc checker {MolID lMin H} {
	#
	#	Checks the inputs to make sure they're with parameters for future procedures
	#
	#	Arguments:
	#	Lmin (Integer): Length of blobs should be an integer between 2 and some number
	#	H* (Float):	Hydropathy scale, must be between 0 and 1 
	#	MolID (Integer): Makes sure there's a top atom to select 
	#	Hydropathy Scale (Array): Specifc scale that the package can use
	#	Results:
	#	The result is that each input will be cleared for future procedures
	set lower [string tolower $MolID]
	set sel [atomselect $lower alpha]
	set sorted [lsort -unique [$sel get chain]]
	if { [llength $sorted] != 1 } {
		puts "Protein has multiple chains use at own risk"
		}
	set res [$sel get resname]
	if {$lMin < 1} {
		puts "Lmin too short"
		return -1
	}
	if {$lMin > [llength $res]} {
		puts "Lmin too long"
		return -1
	}
	if { ($H > 1) || ( $H < 0 )} {
		puts "Hydropathy must be between 0 and 1"
		return -1
	}
	$sel delete 
	return 0
}

proc getSequence {MolID} {
#
#	Acquires the MolID and makes a list of the amino acid residues
#
#	Arguments:
#	MolID (integer): number used to organize molecule files in vmd use 
#	this to call our desired protein
#	Results:
#	Results should be a list that has every resname in the protein seqeunce
#	in order
    set lower [string tolower $MolID]
    set sel [atomselect $lower alpha]
    set resSeq [$sel get resname]
    $sel delete
    puts "sequence works!"
    return $resSeq
}

proc hydropathyScores { hydropathyList Sequence } {
#
#	Takes the sequence and compares to normalized hydropathy scale making a list of scores 
#
#	Arguments 
#	hydropathyList (dict): A dictionary where the amino acids are the keys and the value is a normalized hydropathy list
#   Sequence (list): A list of amino acids from the molecule in vmd
#
#   Results 
#	The result is a list that has the hydropathy scores
	
	set hydroScored {}
	foreach amino $Sequence {
		if {[lsearch -exact $hydropathyList $amino] == -1} {
			puts "Unkown amino acid ending program"
			return -1
		}
		
		set value [dict get $hydropathyList $amino]
		
		lappend hydroScored $value
	}
	puts "hydroS works!"
	return $hydroScored
}

proc hydropathyMean { hydroScores Sequence} {
#
#	Takes a list of hydropathy scores and creates a list of smoothed hydropathy scores
#
#	Arguments:
#	hydroScores (list): A list of hydro based off a normalized hydropathy scale
#
#	Results:
#	The result is a new list of scores that are averaged between each other
	set hydroList {}
	set isFirst 1
	for { set i 0 } { $i < [expr [llength $hydroScores] -1] } {incr i} {
		if {$isFirst == 1} {
			set isFirst 0
			set indexOfFirstValue [lindex $hydroScores $i] 
			set indexOfSecondValue [lindex $hydroScores [expr $i +1]]
			set avgValue [expr ($indexOfFirstValue + $indexOfSecondValue) /2]
			lappend hydroList $avgValue
			continue
		} 
		if {$isFirst == 0} {
			set	indexOfFirstValue [lindex $hydroScores [expr $i - 1]]
			set indexOfSecondValue [lindex $hydroScores $i] 
			set indexOfLastValue [lindex $hydroScores [expr $i + 1]]
			set avgValue [expr ($indexOfFirstValue + $indexOfSecondValue + $indexOfLastValue) / 3]
			lappend hydroList $avgValue
		}
	}
	
	set indexSecondToLast [lindex $hydroScores end-1]
	set indexOfLastValue [lindex $hydroScores end]
	set lastAvgValue [expr ($indexSecondToLast + $indexOfLastValue) /2]
	lappend hydroList $lastAvgValue
	if {[llength $hydroList] != [llength $Sequence] } {
		puts "Error"
		break
	}
	puts "hydroM works"
	return $hydroList
}
	
proc Digitize { H hydroMean } {
#
#	Takes the seqeunce and compares it to the Hydropathy list, making a list of 1s and 0s 
#	based on if exceeds/meets H or goes below it respecitively 
#	
# 	Arguments:
# 	H (float): Float number between 0 and 1 that the amino sequences will compare to
# 	hydroScores (list): a list of averaged hydropathy scores 
#
#	Results
#	A list of 1 and 0 depending on if the value is past the threshold 
	
	set digList {}
	foreach hy $hydroMean {
		if {$hy < $H } {
			lappend digList 0
		} else {
			lappend digList 1 
		}
	}
	if {[llength $digList] != [llength $hydroMean]} { 
		puts "Error: List do not match"
		return -1
	}
	puts "dig works!"
	return $digList
}                                                                                     	
	
proc blobH { digitizedSeq lMin } {
#
#   Proc will find digitized hblobs based off the lMin parameter 
#   
#	Arguments:
#	digitizedSeq (list): A list of 1's and 0's that are determined by the hydrophobic threshold 
#   lMin (integer): An integer that decided the minimum length of an hblob
#
#   Results: 
#   The procedure should give a list of tuples that indicate where an hblobs starts and ends

	set idx 0 
	set start 0
	set finish 0 
	set count 0
	set blist {}
	set isFirst 1
	
	for {set i 0} {$i < [llength $digitizedSeq]} { incr i } {
		set resDigit [lindex $digitizedSeq $i]
		if {$resDigit == 1} {
			#residue is hydrophobic 
			incr count
			if {$isFirst == 1} {
				set isFirst 0
				set start $i 
			}
			if { $i == [expr [llength $digitizedSeq] -1]} {
				if {$count >= $lMin } {
					set finish $i
					lappend blist "$start $finish {h}"
				} else {
					break
				}
			} 
		} else {
			#residue is not hydrophobic 
			if {$isFirst == 0} {
				#previous residue was hydrophobic
				if { $count >= $lMin } {
					#there were enough hydrophobic residues to form a blob
					set finish [expr $i - 1 ]
					# puts $start
					# puts $finish
					lappend blist "$start $finish {h}"
					} 
			}
			set count 0
			set isFirst 1
		}
	}
	puts "blobh works!"
	return $blist
}

proc blobS { blobList digitizedSeq lMin } {
#
#
#    A procedure that uses the list provided by the blobH procedure to determine short blob locations
#
#    Arguments:
#    blobList (list): A list of tuples that show the location of hblobs  
#    digitizedSeq (list): A list of 1's and 0's that are determined by the hydrophobic threshold 
#	lMin (integer): An integer that decided the minimum length of an hblob
#
#	 Results:
#	 Should add to the blobList of tuples to include s blobs 
	
	
	if {[llength $blobList] == 0} {
		puts "no hblobs found"
		return -1
	}
	set slist {}
	#Checks the beginning of the list for an s blob 
	if {[lindex $blobList 0 0] != 0 } {
		if {[lindex $blobList 0 0] < $lMin  } {
			set start 0
			set finish [expr [lindex $blobList 0 0] -1]
			lappend slist "$start $finish {s}"
			}
		}
	#Checks the end of the list for an s blob 
	if {[lindex $blobList end 1] != [expr [llength $digitizedSeq]-1 ]} {
		set lengthOfseq [expr [llength $digitizedSeq] - 1 ]
		if { [expr $lengthOfseq - [lindex $blobList end 1]] < $lMin } {
			set start [expr [lindex $blobList end 1] +1] 
			set finish [expr [llength $digitizedSeq] -1 ]
			lappend slist "$start $finish {s}"
		} 
	}

	#Looks between the hblobs, from previous proc, to see gaps less than the Lmin  	
	for {set i 0} {$i < [expr [llength $blobList] -1 ]} { incr i } {
		set endOffirlist [lindex $blobList $i 1]
		set startOfseclist [lindex $blobList [expr $i + 1] 0]
		if { [expr $startOfseclist - $endOffirlist] <= $lMin  } {
			set start [expr $endOffirlist + 1 ]
			set finish [expr $startOfseclist - 1]
			lappend slist "$start $finish {s}"
		} else {
			continue
		}
	}
	foreach sb $slist {
		lappend blobList $sb
	}
	set blobList [lsort -index 0 $blobList] 
	puts "blobs works!"
	return $blobList
}

proc blobP { blobList digitizedSeq } {
#
#   Returns a list of s, h, and p that determine the hydrophobic region
#
#   Arguments:
#	blobList (list): A list of tuples that show the ranges of s and h blobs 
#   digitizedSeq (list): A list of 1's and 0's that are determined by the hydrophobic threshold 
#
#   Results:
#   Proc should return a list of s, h, and p using the bloblist as a guide
	
 	set isFirst 0
 	set hpsList {}
 	if { $blobList == -1 } {
 		foreach q $digitizedSeq {
 			lappend hpsList "p"
 		}
 		return $hpsList
 	}
 		
 	foreach b $digitizedSeq {
 		lappend hpsList "q"
 	}
 		 
 	set i 0 
 	#Goes through created list and replaces q with h or s 
 	while {$i <= [expr [llength $blobList]-1]} {
 	for {set count [lindex $blobList $i 0]} { $count <= [lindex $blobList $i 1]} {incr count} {
 		set hpsList [lreplace $hpsList $count $count [lindex $blobList $i 2]]
 	}
	incr i
 	}
 	#Goes through created list and turns remaining q's to p
 	for {set j 0} { $j < [llength $hpsList]} {incr j} {
 		if {[lindex $hpsList $j] == "q"} {
 			set hpsList [lreplace $hpsList $j $j "p"]
 		} else {
 			continue
 		}
 	}
 	if {[string match -nocase *q $hpsList] == 1} {
 		puts "error: illegal character"
 		break
 	}
 	puts "blobp works!"
 	return $hpsList
 }
 	
proc blobAssign { blob } {
#
#	Takes a list of h's, s's , and p's and returns a set of numbers corresponding to 1 as h, 2 as s, and 3 as p.
#
#	Arguments:
#	blob (list): A list of h's, s's, and p's	
#
#	Results:
#	A list of values that can be applied to the user filed in vmd
	
	#Creating a list of numbers where 1 is h, 2 is s, and 3 is p
	set numAssignBlob {}
	foreach bp $blob {
	if {$bp == "h"} {
		lappend numAssignBlob 1
	}
	if {$bp == "s"} {
		lappend numAssignBlob 2
	}
	if {$bp == "p"} {
		lappend numAssignBlob 3
	}
	}
	puts "blobAssign works!"
	return $numAssignBlob
}
	
