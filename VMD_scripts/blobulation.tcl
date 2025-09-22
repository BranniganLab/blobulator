# blobulation.tcl
#
###Abstract 
# This file takes a protein sequence and creates user values that are assign to blob type
# h's are for hydrophobic blobs, s's are for short blobs, and p's are for polar blobs 
source normalized_hydropathyscales.tcl
namespace eval ::blobulator:: {
	variable framesOn 0
	variable framesTotal 1
	variable sortedChains {}
	

} 
atomselect macro canonAA {resname ALA ARG ASN ASP CYS GLN GLU GLY HIS HID HIE ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL}

#
#	Proc that blobulates by a sequence range
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	resStart (Integer): An integer that indexes the starting point of the blobulation sequence
#	resEnd (Integer): An integer that indexes the ending point of the blobulation sequence
#
#	Returns:
#	blobulatedSequence (List): A blobulated sequence that is in 1's 2's and 3's
proc ::blobulator::blobulate {MolID lMin H select dictInput} {
	# Source is in the proc so the GUI can call both 
	source normalized_hydropathyscales.tcl
	set nocaseMolID [string tolower $MolID]
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

	set chainBlobs {}
	set chainBlobIndex {}
	set chainBlobGroup {}
	set ::blobulator::sortedChains [::blobulator::getSelect $MolID $select]
	foreach chain $::blobulator::sortedChains {
		set check [atomselect $nocaseMolID "alpha and protein and canonAA and chain $chain"]
		set minimum_residue_length 3
		if {[llength [$check get resname]] < $minimum_residue_length} {
			puts "Ignoring chain $chain, too small to blobulate"
			set idxOfChain [lsearch $::blobulator::sortedChains $chain]
			set ::blobulator::sortedChains [lreplace $::blobulator::sortedChains $idxOfChain $idxOfChain]
			
		}
		$check delete
	}
		
		
	for {set chainNum 0} {$chainNum < [llength $::blobulator::sortedChains] } { incr chainNum} {
		set singleChain [lindex $::blobulator::sortedChains $chainNum] 

		set chainReturn [::blobulator::blobulateChain $MolID $lMin $H $singleChain $usedDictionary]
			if { $chainReturn == -1} {
			break
			return -1
		}	
		set blobulatedSequence [lindex $chainReturn 0]
		
		set index [lindex $chainReturn 1]

		foreach bb $blobulatedSequence {
			lappend chainBlobs $bb
			
		} 

		set chainIndex [::blobulator::blobIndex $blobulatedSequence ]
		foreach ci $chainIndex { 
			lappend chainBlobIndex $ci
		}
		
		
		
		set completeIndex [::blobulator::blobIndex $blobulatedSequence ]
		

		
		
		
	
		
		
	}
	
	if {$chainBlobs != -1} {
	::blobulator::blobUserAssign $chainBlobs $MolID $::blobulator::sortedChains
	::blobulator::blobUser2Assign $chainBlobIndex $MolID $::blobulator::sortedChains

	


	}
	
	return 
}

#
#	Proc that blobulates a specific chain
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
	
	set hBlobRegex "1{$lMin,}"

	set pBlobRegex "\[10]{$lMin,}"

	set sBlobRegex "\[10]{1,$lMin}"

	set sequence [::blobulator::getSequenceChain $MolID $Chain]
	
	set hydroS [::blobulator::hydropathyScores $usedDictionary $sequence]
	if {$hydroS == -1} {
		return -1
		}
	set smoothHydro [::blobulator::hydropathyMean $hydroS $sequence]
	
	set digitized [::blobulator::digitize $H $smoothHydro ]
	
	set stringDigitized [join $digitized ""] 
	

	set hBlobString [blobMaker $stringDigitized $hBlobRegex h $lMin]
	
	set hBlobAndpBlobString [blobMaker $hBlobString $pBlobRegex p $lMin] 
	
	set hBlobAndPblobAndSblobString [blobMaker $hBlobAndpBlobString $sBlobRegex s $lMin]
	
	set hBlobAndPblobAndSblobString [split $hBlobAndPblobAndSblobString ""]
	
	set groupedBlobs [::blobulator::blobGroup $hBlobAndPblobAndSblobString ]

    set blobulatedSequence [::blobulator::blobAssign $hBlobAndPblobAndSblobString]
    	
	return [list $blobulatedSequence $hBlobAndPblobAndSblobString]
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
	set sel [atomselect $nocaseMolID "alpha and protein and canonAA"]
	set sortedChains [lsort -unique [$sel get chain]]
	
	if {[molinfo $MolID get numframes] > 1} {
		set ::blobulator::framesOn 1
		set ::blobulator::framesTotal [molinfo $MolID get numframes]
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
	if { [llength $sortedChains] != 1 } {
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
    set sel [atomselect $nocaseMolID "alpha and protein and canonAA"]
    set resSeq [$sel get resname]
    $sel delete
    
    return $resSeq
}

#
#	Proc that only grabs a sequence from a resid range
#
#	Arguments:
#	MolID (integer): number used to organize molecule files in vmd use this to call our desired protein
#	resStart (Integer): An integer that indexes the starting point of the blobulation sequence
#	resEnd (Integer): An integer that indexes the ending point of the blobulation sequence
#
#	Returns:
#	resSeq (List): A list of three letter amino acid sequences
proc ::blobulator::getSelect {MolID select} {

	set nocaseMolID [string tolower $MolID]

    set sel [atomselect $nocaseMolID "$select" ]
    set sortedChains [lsort -unique [$sel get chain]]
    

  	
    
    $sel delete

    return $sortedChains
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
        set sel [atomselect $lower "alpha and protein and canonAA and chain $Chain"]
        set resSeq [$sel get resname]
        $sel delete
        
        return $resSeq
}

#
#	Takes the sequence and compares to normalized hydropathy scale making a list of scores 
#
#	Arguments 
#	hydropathyDict (dict): A dictionary where the amino acids are the keys and the value is a normalized hydropathy list
#   Sequence (list): A list of amino acids from the molecule in vmd
#
#   Results 
#	The result is a list that has the hydropathy scores
proc ::blobulator::hydropathyScores { hydropathyDict Sequence } {

	
	set hydroScoreList {}
	foreach amino $Sequence {
		
		if {[lsearch $hydropathyDict $amino] == -1} {
			
			if {$amino == "HID" || $amino == "HIE"} {
				set value [dict get $hydropathyDict "HIS"]
			} else {
				set unknownResidueList {}
				foreach aa $Sequence {
					if {[lsearch $hydropathyDict $aa] == -1 } {
						lappend unknownResidueList $aa
					}
					
				}
				puts "Unknown sequence(s) detected: $unknownResidueList \nEnding Program"
				return -1
				}
			
			
		} else {
			set hydroScore [dict get $hydropathyDict $amino] 
		}
		lappend hydroScoreList $hydroScore
	}
	
	return $hydroScoreList
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
	
	set meanHydroList {}
	set denominatorEnds 2
	set denominator 3
	set indexOfFirstValue [lindex $hydroScores 0] 
	set indexOfSecondValue [lindex $hydroScores [expr 1]]
	set avgValue [expr ($indexOfFirstValue + $indexOfSecondValue) / $denominatorEnds]
	lappend meanHydroList $avgValue
	for { set scoreIndex 1 } { $scoreIndex < [expr [llength $hydroScores] -1] } {incr scoreIndex} {
			set	indexOfFirstValue [lindex $hydroScores [expr $scoreIndex - 1]]
			set indexOfSecondValue [lindex $hydroScores $scoreIndex] 
			set indexOfLastValue [lindex $hydroScores [expr $scoreIndex + 1]]
			set avgValue [expr ($indexOfFirstValue + $indexOfSecondValue + $indexOfLastValue) / $denominator]
			lappend meanHydroList $avgValue
	}
	set indexSecondToLast [lindex $hydroScores end-1]
	set indexOfLastValue [lindex $hydroScores end]
	set lastAvgValue [expr ($indexSecondToLast + $indexOfLastValue) / $denominatorEnds]
	lappend meanHydroList $lastAvgValue
	if {[llength $meanHydroList] != [llength $Sequence] } {
		puts "Error: Number of hydropathy scores doesn't match the number of sequences"
		return
	}
	
	return $meanHydroList
}


#
#	Takes the seqeunce and compares it to the Hydropathy list, making a list of 1s and 0s 
#	based on if exceeds/meets H or goes below it respecitively 
#	
# 	Arguments:
# 	H (float): Float number between 0 and 1, this number is the minimum value requirement to become a hydrophobic residue
# 	hydroScores (list): a list of averaged hydropathy scores 
#
#	Results
#	A list of 1 and 0 depending on if the value is past the threshold 
proc ::blobulator::digitize { H smoothHydroMean } {

	
	set digList {}
	foreach smoothedHydroValue $smoothHydroMean {
		if {$smoothedHydroValue < $H } {
			lappend digList 0
		} else {
			lappend digList 1 
		}
	}
	if {[llength $digList] != [llength $smoothHydroMean]} { 
		puts "Error: List do not match"
		return -1
	}
	
	return $digList
}                                                                                     	

#
#	Proc that converts digitized list into a string of h's p's and s's using regular expressions
#
#	Arguments:
#	digiList: A list of 1's and 0's 
#	regPat: The regular expression used to convert binary to letters
#	letter: The letter that the regular expression replaces the binary to
#	lmin: The length threshold required to be an h blob or p blob
#
#	Returns:
#	A list of h's p's and s's indicating blobs
proc blobMaker {digiList regPat letter lmin} {
	
	set newDigiList $digiList
	
	set i 0
	while {$i < [llength [regexp -all -inline $regPat $digiList]]} {
		
		set regMatch [regexp -inline $regPat $newDigiList]
		set hLen [string length $regMatch]
		set replacementStr [string repeat $letter $hLen]
		set newDigiList [regsub $regPat $newDigiList $replacementStr]
		
		incr i
	}
	
return $newDigiList
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
	set index 0
	set indexList {}
	

	for {set i 0 } { $i < [llength $blob]} { incr i } {
		set currentChar [lindex $blob $i]
		
		
		if { $currentChar != $blobChar } {
			set blobChar $currentChar
			incr index 
			lappend indexList $index
			
		} else {
			lappend indexList $index
		}
		
	}


		
return $indexList
			 
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

#
#	Takes a generated list of 1, 2, and 3s and assigns each residue a user value relating to these numbers, but only for relevant chains
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for
#	blob1 (List): A list of 1's, 2's, and 3's. The 1's represent h's the 2's represent s's and the 3's represent p's
#	chainList (List): A list of chains for a protein that the user values will assign to
proc ::blobulator::blobUserAssign {blob1 MolID chainList} {
	
	
	set molid [string tolower $MolID]
	set clean [atomselect $molid all]
	$clean set user 0
	$clean delete
	set blobGroupNumber 3
	
	for {set frame 0} {$i <= $::blobulator::framesTotal} {incr frame} {
		set sel [atomselect $molid "protein and canonAA and alpha and chain $chainList"]
		$sel frame $frame
		$sel set user $blob1
		$sel delete
	}

	
	
	for {set frame 0} {$i <= $::blobulator::framesTotal} {incr frame} {
		for {set blobType 1} { $blobType <= $blobGroupNumber } {incr blobType} {
			set sel [atomselect $molid "user $blobType"]
			set residues [$sel get residue]
			$sel delete
			if {[llength $residues] > 1} {
				foreach rs $residues {
					set sel2 [atomselect $molid "residue $rs and protein"]
					$sel2 frame $frame
					$sel2 set user $blobType
					$sel2 delete
				}
				
			
			
		}
	}
		
  }
	  

}


#
#	Takes a generated list of 1, 2, and 3s and assigns each residue a user value relating to these numbers, but only for relevant chains
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for
#	blob1 (List): A list of 1's, 2's, and 3's. The 1's represent h's the 2's represent s's and the 3's represent p's
#	chainList (List): A list of chains for a protein that the user values will assign to
proc ::blobulator::blobUser2Assign { blob2 MolID chainList} {
	set molid [string tolower $MolID]
	set clean [atomselect $molid all]
	$clean set user2 0
	$clean delete
	
	set sel [atomselect $molid "protein and canonAA and alpha and chain $::blobulator::sortedChains"]

	$sel set user2 $blob2
	$sel delete

	set blobLength [llength [lsort -unique $blob2]]
	for {set blobNum 1} { $blobNum<= $blobLength } { incr blobNum} {
		set sel [atomselect $molid "user2 $i"]
		set residues [$sel get residue]
		$sel delete
	
		foreach rs $residues {
			

			set sel2 [atomselect $molid "residue $rs and protein"]
			$sel2 set user2 $i
			$sel2 delete
		}
	
	}
	set numOfFrames [molinfo $molid get numframes]
	::blobulator::blobTrajUser2 $numOfFrames $blob2 $MolID
}

#
#	Takes a generated list of numbers and applies user values across a trajectory
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for
#	blob2 (List): A list of numbers that represent the number of groups in the protein
#	frames (Intger): An integer representing the number of frames in a trajectory
proc ::blobulator::blobTrajUser {frames blob1 MolID} {
	
	set blobLength [llength [lsort -unique $blob1]]
	
	set userList {}

	set sel [atomselect $MolID "user 1 or user 2 or user 3 "]
	
	set user [$sel get user]
	
	lappend userList {*}$user

	$sel delete
	
	
	

	
	set sel2 [atomselect $MolID "protein and canonAA and chain $::blobulator::sorted"]
	for {set i 0} { $i <= $frames} {incr i} {
		
		$sel2 frame $i
		$sel2 set user $userList
	
		
	}
	$sel2 delete
}


#
#	Takes a generated list of numbers and applies user values across a trajectory
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for
#	blob2 (List): A list of numbers that represent the number of groups in the protein
#	frames (Intger): An integer representing the number of frames in a trajectory
proc ::blobulator::blobTrajUser2 {totalFrames blob2 MolID} {
	
	set blobLength [llength [lsort -unique $blob2]]
	set user2List {}
	for {set blobNum 1} {$blobNum<= $blobLength} {incr blobNum} {
		set sel [atomselect $MolID "user2 $blobNum"]
		
		set user2 [$sel get user2]
		
		lappend user2List {*}$user2

		$sel delete
	}
	
	
	set sel2 [atomselect $MolID "protein and canonAA and chain $::blobulator::sortedChains"]
	for {set frame 0} { $frame <= $totalFrames} {incr frame} {
		
		$sel2 frame $frame
		$sel2 set user2 $user2List
	
		
	}
	$sel2 delete
}


# proc blobUser3Assign { blob3 MolID } {
# 	set lower [string tolower $MolID]
# 	set sel [atomselect $lower "alpha and protein" ]
# 	$sel set user3 $blob3 
# 	$sel delete 
# }



