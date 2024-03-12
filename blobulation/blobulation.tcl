set bi_list [list 0 0 1 1 1 1 0 0 1 0 1 0 1 0 1 1 1 1 0 0 0 1 1 1 1 0 0 0 ]



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
	#code currently doesn't account for ending blobs 
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
	if {[lindex $blobList 0 0] != 0 } {
		if {[lindex $blobList 0 0] < $lMin  } {
			set start 0
			set finish [expr [lindex $blobList 0 0] -1]
			lappend slist "$start $finish {s}"
			}
		}
	if {[lindex $blobList end 1] != [expr [llength $digitizedSeq]-1 ]} {
		
		set lengthOfseq [expr [llength $digitizedSeq] - 1 ]
		if { [expr $lengthOfseq - [lindex $blobList end 1]] < $lMin } {
			
			set start [expr [lindex $blobList end 1] +1] 
			set finish [expr [llength $digitizedSeq] -1 ]
			lappend slist "$start $finish {s}"
		} 
	}

		
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
 	
 	while {$i <= [expr [llength $blobList]-1]} {
 	
 	
 	for {set count [lindex $blobList $i 0]} { $count <= [lindex $blobList $i 1]} {incr count} {
 		
 		
 		set blob_list [lreplace $blob_list $count $count [lindex $blobList $i 2]]
 		
 	}
 	
	incr i
 	
 	}
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
 	
 
