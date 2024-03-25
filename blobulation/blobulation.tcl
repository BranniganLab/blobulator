source normalized_hydropathyscales.tcl

puts "Enter MolID"
gets stdin MolID
puts $MolID
puts "Enter Lmin"
gets stdin lMin
puts $lMin
puts "Enter H"
gets stdin H
puts $H


proc checker {MolID lMin H } {
	#
	#	Checks the inputs to make sure they're with parameters for future procedures
	#
	#	Arguments:
	#	Lmin (Integer) Length of blobs should be an integer between 2 and some number
	#	H* (Float)	Hydropathy scale, must be between 0 and 1 
	#	MolID (integer) Makes sure there's a top atom to select 
	#	Hydropathy Scale (Array) Specifc scale that the package can use
	#	Results:
	#	The result is that each input will be cleared for future procedures
	set sel [atomselect $MolID alpha]
	set res [$sel get resname]
	if {$lMin <= 1} {
		puts "Lmin too short"
		return -1
	}
	if {$lMin >= [llength $res]} {
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
	
set checked [checker $MolID $lMin $H]
	if {$checked == -1} {
		puts "Variables are incorrect ending program"
		return -1  
	}

proc tcl::getSequence {MolID} {
#
#	Acquires the MolID and makes a list of the amino acid residues
#
#	Arguments:
#	MolID (integer) number used to organize molecule files in vmd use 
#	this to call our desired protein
#	Results:
#	Results should be a list that has every resname in the protein seqeunce
#	in order
    
    set sel [atomselect $MolID alpha]

    set stuff [$sel get resname]
    $sel delete
    return $stuff
}

set sequence [tcl::getSequence $MolID]
puts "sequence works!"

proc hydropathyMean { Hydropathylist Sequence } {
#
#	Takes the seqeunce and compares to normalized hydropathy scale will create average scores 
#
#	Arguments 
#	Hydropathylist (dict) A dictionary where the amino acids are the keys and the value is a normalized hydropathy list
#   Sequence (list) A list of amino acids from the molecule in vmd
#
#   Results 
#	The result is a list that has the smoothed hydropathy scores
	
	set mylist {}
	foreach amino $Sequence {
		if {[lsearch -exact $Hydropathylist $amino] == -1} {
			puts "Unkown amino acid ending program"
			return -1
		}
		
		set value [dict get $Hydropathylist $amino]
		
		lappend mylist $value
	}
	
	
	set hydrolist {}
	set isFirst 1
	for { set i 0 } { $i < [expr [llength $mylist] -1] } {incr i} {
		if {$isFirst == 1} {
			set isFirst 0
			set firstvalue [lindex $mylist $i] 
			set secondvalue [lindex $mylist [expr $i +1]]
			set firstvaluefinal [expr ($firstvalue + $secondvalue) /2]
			
			lappend hydrolist $firstvaluefinal
			
			
			continue
		} 
		if {$isFirst == 0} {
			set	preceedingvalue [lindex $mylist [expr $i - 1]]
			
			set initialvalue [lindex $mylist $i] 
			
			set aheadervalue [lindex $mylist [expr $i + 1]]
			

			
			set valuefinal [expr ($preceedingvalue + $initialvalue + $aheadervalue) / 3]
		
			
			lappend hydrolist $valuefinal
			

		}

	}
	set sectolastvalue [lindex $mylist end-1]
	set lastvalue [lindex $mylist end]
	set lastvaluefinal [expr ($sectolastvalue + $lastvalue) /2]
	
	lappend hydrolist $lastvaluefinal
	

	if {[llength $hydrolist] != [llength $Sequence] } {
		puts "Error"
		break
	}
		
	
	return $hydrolist
	
	}

set hydro [hydropathyMean $KD_Normalized $sequence]
	if {$hydro == -1} {
	return -1
	}
	
puts "hydro works!"
	

	
proc Digitize { H Hydroscores } {
#
#	Takes the seqeunce and compares it to the Hydropathy list, making a list of 1s and 0s 
#	based on if exceeds/meets H or goes below it respecitively 
#	
# 	Arguments:
# 	H (float): Float number between 0 and 1 that the amino sequences will compare to
# 	Hydroscores (list): a list of averaged hydropathy scores 
#
#	Results
#	A list of 1 and 0 depending on if the value is past the threshold 
	
	set myist {}
	foreach hy $Hydroscores {
		
		
		
		if {$hy < $H } {
			lappend mylist 0
		} else {
			lappend mylist 1 
		}
	}

	if {[llength $mylist] != [llength $Hydroscores]} { 
		puts "Error: List do not match"
		break
	}
	
	return $mylist
}                                                                                     	
	
set dig [Digitize $H $hydro ]
	puts "dig works!"	
	
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

	return $blist
}
set blobh [ blobH $dig $lMin ]
	puts "blobh works!"

proc blobS { blobList digitizedSeq lMin } {
#
#
#    A procedure that uses the list provided by the blobH procedure to determine short blob locations
#
#    Arguments:
#    blobList (list): A list of tuples that show the location of hblobs  
#    digitizedSeq (list): A list of 1's and 0's that are determined by the hydrophobic threshold 
#	 lMin (integer): An integer that decided the minimum length of an hblob
#
#	 Results:
#	 Should add to the blobList of tuples to include s blobs 

	puts $blobList
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
		
		if { [expr $startOfseclist - $endOffirlist] <= 4  } {
			
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
set blobs [ blobS $blobh $dig $lMin ]
puts "blobs works!"

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
 	set blob_list {}
 	foreach b $digitizedSeq {
 		lappend blob_list "q"
 	}
 	
 	set i 0 
 	#Goes through created list and replaces q with h or s 
 	while {$i <= [expr [llength $blobList]-1]} {
 	for {set count [lindex $blobList $i 0]} { $count <= [lindex $blobList $i 1]} {incr count} {
 		set blob_list [lreplace $blob_list $count $count [lindex $blobList $i 2]]
 	}
	incr i
 	}
 	#Goes through created list and turns remaining q's to p
 	for {set j 0} { $j < [llength $blob_list]} {incr j} {
 		if {[lindex $blob_list $j] == "q"} {
 			set blob_list [lreplace $blob_list $j $j "p"]
 		} else {
 			continue
 		}
 	}

 	
 	if {[string match -nocase *q $blob_list] == 1} {
 		puts "error: illegal character"
 		break
 	}
 	puts $digitizedSeq
 	return $blob_list

 	}
 	
set blobp [ blobP $blobs $dig ]
puts "blobp works!"

proc blob { blob } {
#
#	Takes a list of h's, s's , and p's and returns a set of numbers corresponding to 1 as h, 2 as s, and 3 as p.
#
#	Arguments:
#	blob (list): A list of h's, s's, and p's	
#
#	Results:
#	A list of values that can be applied to the user filed in vmd
	
	
	#Creating a list of numbers where 1 is h, 2 is s, and 3 is p
	set numberassignblobs {}
	foreach bp $blob {
	if {$bp == "h"} {
	lappend numberassignblobs 1
	}
	if {$bp == "s"} {
	lappend numberassignblobs 2
	}
	if {$bp == "p"} {
	lappend numberassignblobs 3
	}
	}
	puts $blob
	return $numberassignblobs
}

set blobulated [blob $blobp]
puts $blobulated	
#Makes sure procedures that fail to pass checks can assign values. 
if {$blobulated != -1} {
	
	set sel [atomselect $MolID alpha]
	$sel set user $blobulated
	$sel get user
	$sel delete
	} 
	
