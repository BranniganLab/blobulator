# blobulation.tcl
#
###Abstract 
# This file takes a protein sequence and creates user values that are assign to blob type
# h's are for hydrophobic blobs, s's are for short blobs, and p's are for polar blobs 
namespace eval ::blobulator:: {} 
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
proc ::blobulator::blobulate {MolID lMin H dictInput} {
	
	set noCaseDictInput [string tolower $dictInput]
	source normalized_hydropathyscales.tcl
	if {$dictInput == "Kyte-Doolittle"} {
		set usedDictionary $KD_Normalized
	}

	if {$dictInput == "Moon-Fleming"} {
		set usedDictionary $MF_Normalized
	}

	if {$dictInput == "Eisenberg-Weiss"} {
		set usedDictionary $EW_Normalized
	}
	set argumentsOK [::blobulator::checker $MolID $lMin $H]
	if {$argumentsOK == -1} {
		puts "Variables are incorrect ending program"
		return  
		}
	if {$argumentsOK == 1} { 
		
		set nocaseMolID [string tolower $MolID]
		set sel [atomselect $nocaseMolID alpha]
		set sorted [lsort -unique [$sel get chain]]
		

		set chainBlobs {}
		set chainBlobIndex {}
		set chainBlobGroup {}
		for {set i 0} {$i < [llength $sorted] } { incr i} {
			set singleChain [lindex $sorted $i] 
			set chainReturn [::blobulator::blobulateChain $MolID $lMin $H $singleChain $usedDictionary]
				if { $chainReturn == -1} {
				break
				return -1
			}
			set blobulated [lindex [::blobulator::blobulateChain $MolID $lMin $H $singleChain $usedDictionary] 0]
		
			set index [lindex [::blobulator::blobulateChain $MolID $lMin $H $singleChain $usedDictionary] 1]
			foreach bb $blobulated {
				lappend chainBlobs $bb
				
			} 

			set chainIndex [::blobulator::::blobulator::blobIndex $blobulated ]
			foreach ci $chainIndex { 
				lappend chainBlobIndex $ci
			}
			
			set chainGroup [::blobulator::blobGroup $index]
			foreach cg $chainGroup {
				lappend chainBlobGroup $cg
			}
			#puts $chainGroup
			
			
			
		}
		if {$chainBlobs != -1} {
			::blobulator::blobUserAssign $chainBlobs $MolID
			::blobulator::blobUser2Assign $chainBlobIndex $MolID
			blobUser3Assign $chainBlobGroup $MolID
		
		
		}
		return $blobulated
		} else {
		
	set sequence [::blobulator::getSequence $MolID]
	set hydroS [::blobulator::hydropathyScores $usedDictionary $sequence]
	if {$hydroS == -1} {
		return -1
		}
	set smoothHydro [::blobulator::hydropathyMean $hydroS $sequence]
	set digitized [::blobulator::digitize $H $smoothHydro ]
	set hblob [ ::blobulator::hBlob $digitized $lMin ]
	set hsblob [ ::blobulator::hsBlob  $hblob $digitized $lMin ]
	set hpsblob [ ::blobulator::hpsBlob  $hsblob $digitized ]
	set groupedBlob [::blobulator::blobGroup $hpsblob]
	set blobulated [::blobulator::blobAssign $hpsblob]
	set ::blobulator::blobIndexList [ ::blobulator::blobIndex $blobulated ]
	if {$blobulated != -1} {
		::blobulator::blobUserAssign $blobulated $MolID
		::blobulator::blobUser2Assign $::blobulator::blobIndexList $MolID
		blobUser3Assign $groupedBlob $MolID
	}
	#Makes sure procedures that fail to pass checks can't assign values. 

	
	return $blobulated
	}
}
#
#	Proc that subsitiutes the blobulate task if multiple chains in a protein are detected
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	Chain (List): A list of each chain name used to parse through specific chains seperately
#
#	Results:
#	The results is a user value applied to the protein of choice the differentiates h blobs, p blobs, and s blobs. 
proc ::blobulator::blobulateChain {MolID lMin H Chain usedDictionary} {
	source normalized_hydropathyscales.tcl
	set sequence [::blobulator::getSequenceChain $MolID $Chain]
	set hydroS [::blobulator::hydropathyScores $usedDictionary $sequence]
	if {$hydroS == -1} {
		return -1
		}
	set smoothHydro [::blobulator::hydropathyMean $hydroS $sequence]
	set digitized [::blobulator::digitize $H $smoothHydro ]
	set hblob [ ::blobulator::hBlob $digitized $lMin ]
	set hsblob [ ::blobulator::hsBlob  $hblob $digitized $lMin ]
	set hpsblob [ ::blobulator::hpsBlob  $hsblob $digitized ]
	set groupedBlobs [::blobulator::blobGroup $hpsblob ]
    set blobulated [::blobulator::blobAssign $hpsblob]
    	
	return [list $blobulated $hpsblob]
	}	

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
proc ::blobulator::checker {MolID lMin H} {

	set nocaseMolID [string tolower $MolID]
	set sel [atomselect $nocaseMolID "alpha and protein"]
	set sorted [lsort -unique [$sel get chain]]
	
		
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
	if { [llength $sorted] != 1 } {
		return 1
	}
	$sel delete 
	return 0
}

#
#	Acquires the MolID and makes a list of the amino acid residues
#
#	Arguments:
#	MolID (integer): number used to organize molecule files in vmd use 
#	this to call our desired protein
#	Results:
#	Results should be a list that has every resname in the protein seqeunce
#	in order
proc ::blobulator::getSequence {MolID} {

    set nocaseMolID [string tolower $MolID]
    set sel [atomselect $nocaseMolID "alpha and protein"]
    set resSeq [$sel get resname]
    $sel delete
    
    return $resSeq
}
#
#	Acquires the MolID and makes a list of the amino acid residues
#
#	Arguments:
#	MolID (integer): number used to organize molecule files in vmd use 
#	this to call our desired protein
#	Results:
#	Results should be a list that has every resname in the protein seqeunce
#	in order
proc ::blobulator::getSequenceChain {MolID Chain} {
	set lower [string tolower $MolID]
        set sel [atomselect $lower "alpha and chain $Chain"]
        set resSeq [$sel get resname]
        $sel delete
        
        return $resSeq
}

#
#	Takes the sequence and compares to normalized hydropathy scale making a list of scores 
#
#	Arguments 
#	hydropathyList (dict): A dictionary where the amino acids are the keys and the value is a normalized hydropathy list
#   Sequence (list): A list of amino acids from the molecule in vmd
#
#   Results 
#	The result is a list that has the hydropathy scores
proc ::blobulator::hydropathyScores { hydropathyList Sequence } {

	
	set hydroScored {}
	foreach amino $Sequence {
		if {[lsearch -exact $hydropathyList $amino] == -1} {
			
			if {$amino == "HID" || $amino == "HIE"} {
				set value [dict get $hydropathyList "HIS"]
			} else {
				set unknownResidueList {}
				set count 0
				foreach aa $Sequence {
					if {[lsearch -exact $hydropathyList $aa] == -1 } {
						lappend unknownResidueList $aa
					}
					
				}
				puts "Unknown sequence(s) detected: $unknownResidueList \nEnding Program"
				return -1
				}
			
			
		} else {
		set value [dict get $hydropathyList $amino] 
		}
		lappend hydroScored $value
	}
	
	return $hydroScored
}


#
#	Takes a list of hydropathy scores and creates a list of smoothed hydropathy scores
#
#	Arguments:
#	hydroScores (list): A list of hydro based off a normalized hydropathy scale
#
#	Results:
#	The result is a new list of scores that are averaged between each other
proc ::blobulator::hydropathyMean { hydroScores Sequence} {

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
	
	return $hydroList
}


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
proc ::blobulator::digitize { H smoothHydroean } {

	
	set digList {}
	foreach hy $smoothHydroean {
		if {$hy < $H } {
			lappend digList 0
		} else {
			lappend digList 1 
		}
	}
	if {[llength $digList] != [llength $smoothHydroean]} { 
		puts "Error: List do not match"
		return -1
	}
	
	return $digList
}                                                                                     	

#
#   	Proc will find digitized hblobs based off the lMin parameter 
#   	
#	Arguments:
#	digitizedSeq (list): A list of 1's and 0's that are determined by the hydrophobic threshold 
#   	lMin (integer): An integer that decided the minimum length of an hblob
#
#   	Results: 
#  	 The procedure should give a list of tuples that indicate where an hblobs starts and ends	
proc ::blobulator::hBlob { digitizedSeq lMin } {


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
					lappend blist "$start $finish {h}"
					} 
			}
			set count 0
			set isFirst 1
		}
	}
	
	return $blist
}


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
proc ::blobulator::hsBlob  { blobList digitizedSeq lMin } {

	
	
	if {[llength $blobList] == 0} {
		
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
	
	return $blobList
}

#
#   Returns a list of s, h, and p that determine the hydrophobic region
#
#   Arguments:
#	blobList (list): A list of tuples that show the ranges of s and h blobs 
#   digitizedSeq (list): A list of 1's and 0's that are determined by the hydrophobic threshold 
#
#   Results:
#   Proc should return a list of s, h, and p using the bloblist as a guide
proc ::blobulator::hpsBlob  { blobList digitizedSeq } {

	
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
 	
 	return $hpsList
 }

#
#	Takes a list of h's, s's , and p's and returns a set of numbers corresponding to 1 as h, 2 as s, and 3 as p.
#
#	Arguments:
#	blob (list): A list of h's, s's, and p's	
#
#	Results:
#	A list of values that can be applied to the user filed in vmd	
proc ::blobulator::blobAssign { blob } {

	
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
	
	return $numAssignBlob
}
#
#	Takes a list of h's p's and s's and assigns them to their own groups, so the first set of s's p's or h's is group 1 and then the next set is group 2 etc. 
#
#	Arguments:
#	blob (list): A list of h's s's and p's
#
#	Results:
#	A list of values that belongs to a group of blobs 
proc ::blobulator::blobIndex { blob } {
	
	
	set blobChar q
	set count 1
	set countList {}
	

	for {set i 0 } { $i < [llength $blob]} { incr i } {
		set currentChar [lindex $blob $i]
		
		
		if { $currentChar != $blobChar } {
			set blobChar $currentChar
			incr count 
			lappend countList $count
			
		} else {
			lappend countList $count
		}
		
	}


		
return $countList
			 
}		
#
#	Takes a list of h's p's and s's and assigns them to their own groups, so the first set of s's p's and h's is group 1 and then the next set is group 2 etc. 
#
#	Arguments:
#	blob (list): A list of h's s's and p's
#
#	Results:
#	A list of values that belongs to a group of blobs 			
proc ::blobulator::blobGroup { blob } {

	set groupList {}
	set hCount 1
	set pCount 1
	set sCount 1
	set activeChar q

	foreach b $blob {
		

		if { $activeChar != $b} {
			set activeChar $b
			upvar 0 ${b}count count 
			incr count
			
			lappend groupList $count
			
		} else {
			upvar 0 ${b}count count
			
			lappend groupList $count

		}
	}

return $groupList
}

proc ::blobulator::blobUserAssign { blob1 MolID } { 
	set molid [string tolower $MolID]
	set clean [atomselect $molid all]
	$clean set user 0
	$clean delete

	set sel [atomselect $molid "alpha and protein"]
	$sel set user $blob1
	$sel delete

	#Only have 3 user values and therefore know how many increments are needed 
	for {set i 1} { $i <= 3 } {incr i} {
		set sel [atomselect $molid "user $i"]
		set resids [$sel get resid]
		$sel delete
		if {[llength $resids] > 1} {
			foreach rs $resids {
				set sel2 [atomselect $molid "resid $rs and protein"]
				$sel2 set user $i
			}
			$sel2 delete
		}
	}
			
	
 }

proc ::blobulator::blobUser2Assign { blob2 MolID } {
	
	set molid [string tolower $MolID]
	set clean [atomselect $molid all]
	$clean set user2 0
	$clean delete

	set sel [atomselect $molid "alpha and protein"]
	$sel set user2 $blob2
	$sel delete

	set blobLength [llength [lsort -unique $blob2]]
	for {set i 1} { $i < $blobLength } { incr i } {
		set sel [atomselect $molid "user2 $i"]
		set resids [$sel get resid]
		$sel delete
	
		foreach rs $resids {
			
			set sel2 [atomselect $molid "resid $rs and protein"]
			$sel2 set user2 $i
		}
	
	} 
}

proc blobUser3Assign { blob3 MolID } {
	set lower [string tolower $MolID]
	set sel [atomselect $lower "alpha and protein" ]
	$sel set user3 $blob3 
	$sel delete 
}



