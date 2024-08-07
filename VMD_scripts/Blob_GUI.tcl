source blobulation.tcl
if [winfo exists .blob] {
	wm deiconify $blobs
	return
}
set buttonWidth 42
set defaultButtonWidth 18
set dropDownMenuWidth 14 
set isFirst 0
set blobColorType1 "Blob Type"
set blobColorType2 "Blob ID"
set hydropathyScale1 "Kyte-Doolittle"
set hydropathyScale2	"Eisenberg-Weiss"
set hydropathyScale3 "Moon-Fleming"

set blobs [toplevel ".blob"]
wm title $blobs "Blobulation"
wm resizable $blobs 0 0
wm attributes $blobs -alpha 1;
wm attributes $blobs -fullscreen 0 
grid [label $blobs.1_MolID -text MolID ]
grid [entry $blobs.tv_MolID -width 10 -textvariable MolID ] -row 0 -column 1
if {$MolID == ""} {
	set MolID "top"
}
set paraList [list Lmin 1 50 1 H .1 1 .01]
foreach { entry min max interval} $paraList {
	set w1 [label $blobs.l_$entry -text $entry]
	set w2 [entry $blobs.e_$entry -width 10 -textvariable $entry]
	set w3 [scale $blobs.s_$entry -orient horizontal -from $min -to $max -length 175 -resolution $interval -tickinterval 0 -variable $entry -showvalue 0]
	
	
	grid $w1 $w2 $w3 	
}
grid [label $blobs.t -text "Blobulate by: " -height 2] -row 4 -column 0 -columnspan 2 -sticky e
grid [ttk::combobox $blobs.dmnu -textvariable graphrep2 -width $dropDownMenuWidth -values [list $blobColorType1 $blobColorType2] -state readonly ] -pady 6 -row 4 -column 2 -sticky w
grid [label $blobs.t2 -text "Hydropathy Scale : " -height 2] -row 5 -column 0 -columnspan 2 -sticky e
grid [checkbutton $blobs.check -text "Auto Update" -variable checkForUpdate -command {blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList}] -row 5 -column 2 -sticky e
grid [ttk::combobox $blobs.dmnu2  -textvariable hydropathyScaleDictionaryList -width $dropDownMenuWidth -values [list $hydropathyScale1 $hydropathyScale2 $hydropathyScale3] -state readonly] -pady 6 -row 5 -column 2 -sticky w
grid [button $blobs.blobulate -text "Blobulate!" -font [list arial 9 bold] -width $buttonWidth -command {blobulation $MolID $Lmin $H $hydropathyScaleDictionaryList} ] -columnspan 3
grid [button $blobs.ldefault -text "Set Lmin Default" -width $buttonWidth -command {lminDefault }] -padx 0  -columnspan 3
grid [button $blobs.hdefault -text "Set H Default" -width $buttonWidth -command {hDefault }] -padx 0 -columnspan 3
grid [button $blobs.clear -text "Clear representations" -width $buttonWidth -command {blobClear $MolID}] -column 0 -columnspan 3

#
#	Checks radiobutton value so blobulate properly displays representations
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#
#	Global Arguments:
#	graphrep2 (List): A list of graph representation options, decided which graphuser proc called depending on what the variable is set to
#	isFirst (Integer): A number that swtiches to 1 when the blobulation proc has been called and 0 when blobulation hasnn't been called
#	blobColorType1 (String): A parameter used for graphrep2 checks, if it is set to this variable, will call graphRepUser proc
#	blobColorType2 (String): A parameter used for graphrep2 checks, if it is set to this variable, will call graphRepUser2 proc
#	blobs (Object): Overarching window frame
proc blobulation { MolID Lmin H hydropathyScaleDictionaryList} {
	global blobs
	global graphrep2 
	global isFirst
	set isFirst 1
	global blobColorType1
	global blobColorType2
	bind $blobs.s_Lmin <ButtonRelease> {blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList} 
	bind $blobs.s_H <ButtonRelease> {blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList} 
	bind $blobs.dmnu <<ComboboxSelected>> {blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList}
	bind $blobs.dmnu2 <<ComboboxSelected>> {hydropathyScaleDropDownMenu $MolID $Lmin $H $hydropathyScaleDictionaryList}
	if {$graphrep2 == $blobColorType1} {
		blobulate $MolID $Lmin $H $hydropathyScaleDictionaryList
		graphRepUser $MolID $Lmin $H 
	} elseif { $graphrep2 == $blobColorType2} {
		blobulate $MolID $Lmin $H $hydropathyScaleDictionaryList
		graphRepUser2 $MolID $Lmin $H 
	} else {
		puts "no value"
	}
return
}


#
#	Runs blobulation when any slider is moved
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
#	
#	Global Arguments:
#	graphrep2 (List): A list of graph representation options, decided which graphuser proc called depending on what the variable is set to
#	isFirst (Integer): A number that swtiches to 1 when the blobulation proc has been called and 0 when blobulation hasnn't been called
#	blobColorType1 (String): A parameter used for graphrep2 checks, if it is set to this variable, will call graphRepUser proc
#	blobColorType2 (String): A parameter used for graphrep2 checks, if it is set to this variable, will call graphRepUser2 proc
proc blobulationSlider { MolID Lmin H hydropathyScaleDictionaryList} {
	global graphrep2 
	global isFirst
	global blobColorType1
	global blobColorType2
	

	if {$isFirst == 1} {

		if {$graphrep2 == $blobColorType1} {
			blobulate $MolID $Lmin $H $hydropathyScaleDictionaryList 
			graphRepUser $MolID $Lmin $H 
		} elseif {$graphrep2 == $blobColorType2} {
			blobulate $MolID $Lmin $H $hydropathyScaleDictionaryList
			graphRepUser2 $MolID $Lmin $H 

		} else {
			puts "no value"
		}
	} else {
		return 
	} 
return
}

#
#	Creates parameters for when the second drop down menu is changed  
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
#
#	Global Arguments:
#	checkForUpdate (Integer): A number that switches to 1 if the checkbox is active and 0 when the checkbox is inactive
proc hydropathyScaleDropDownMenu {MolID Lmin H hydropathyScaleDictionaryList} {
	global checkForUpdate
	if {$checkForUpdate == 1} {
		hDefault
	} else {
		blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList
	}
return
}

#
#	Set Lmin variable to default value, currently 4
#
#	Global Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
proc lminDefault {} {
	global H MolID Lmin hydropathyScaleDictionaryList
	set Lmin 4
	blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList
return
}

#
#	Sets H variable to default value based on dictionary 
#
#	Global Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
#	checkForUpdate (Integer): A number that switches to 1 if the checkbox is active and 0 when the checkbox is inactive
#	blobs (Object): Overarching window frame
proc hDefault {} {
	global H MolID Lmin hydropathyScaleDictionaryList checkForUpdate blobs
	
	if {$hydropathyScaleDictionaryList == "Kyte-Doolittle"} {
		set H .4
	}

	if {$hydropathyScaleDictionaryList == "Eisenberg-Weiss"} {
		set H .28
	}
	if {$hydropathyScaleDictionaryList == "Moon-Fleming"} {
		set H .35
	}

	blobulationSlider $MolID $Lmin $H $hydropathyScaleDictionaryList

	return
}

#
#	Runs graphical representations showing hblobs in QuickSurf, p and s blobs in NewCartoon
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
proc graphRepUser {MolID Lmin H} { 
	
	set range [molinfo $MolID get numreps]
	for {set i 0} { $i < $range } {incr i} {
		mol delrep 0 $MolID
	}  
	set count 0

	set sel [atomselect $MolID protein]
	set user2length [lsort -unique [$sel get user2]]
	$sel delete
	foreach u2 $user2length {

		mol representation QuickSurf 1.21 1 .5 2
		mol material AOChalky
		mol color ColorID 23
		
		

		mol addrep $MolID 
		mol modselect $count $MolID "user 1 and user2 $u2"
		
		incr count 
	}
	

	mol representation NewCartoon .3 20
	mol color ColorID 7
	mol addrep $MolID 
	mol modselect $count $MolID "user 2"
	incr count

	mol representation NewCartoon .3 20 
	mol color ColorID 3
	mol addrep $MolID 
	mol modselect $count $MolID "user 3"
	incr count

	mol representation NewCartoon .3 20 
	mol color ColorID 23
	mol addrep $MolID 
	mol modselect $count $MolID "user 1"
	incr count
return 
}

#
#	Runs graphical representations showing hblobs in QuickSurf (by blob grouping), p and s blobs in NewCartoon
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
proc graphRepUser2 {MolID Lmin H} {
	
	set range [molinfo $MolID get numreps]
	for {set i 0} {$i < $range} {incr i} {
		mol delrep 0 $MolID
	}   
	set count 0
	set sel [atomselect $MolID protein]
	set user2length [lsort -unique [$sel get user2]]
	$sel delete
	foreach u2 $user2length {

		mol representation QuickSurf 1.21 1 .5 2
		mol material AOChalky
		mol color user2
		
		

		mol addrep $MolID 
		mol modselect $count $MolID "user 1 and user2 $u2"
		
		incr count 
	}
	
	
	
	mol representation NewCartoon .3 20
	mol color ColorID 7
	mol addrep $MolID 
	mol modselect $count $MolID "user 2"
	incr count 
	
	mol representation NewCartoon .3 20 
	mol color ColorID 3
	mol addrep $MolID 
	mol modselect $count $MolID "user 3"
	incr count 

	mol representation NewCartoon .3 20 
	mol color user2
	mol addrep $MolID 
	mol modselect $count $MolID "user 1"
	incr count
	colorScale
return
}


#
#	Program removes all graphical representations
# 
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#
#	Global Arguments:
#	isFirst (Integer): A number that swtiches to 1 when the blobulation proc has been called and 0 when blobulation hasnn't been called
proc blobClear {MolID} {
	global isFirst
	set isFirst 0
	set range [molinfo $MolID get numreps]
		for {set i 0} {$i < $range} {incr i} {
			mol delrep 0 $MolID
		} 
return 
	}
	
#
#	Program the destroys the GUI window
#
proc blobQuit {} {
	destroy .blob
return
}

#
#	Function that creates a gradient from each point using the slope function
#
#	Arguments:
# 	PointA (Integer): Starting value used to start i at the desired color num
#	PointB (Integer): Ending value used to end the iteration to 
#	ColorA (List): List of color values, start point that increments up to the end point
# 	ColorB (List): List of color values, end point 
proc tricolor_scale {PointA PointB ColorA ColorB} {
	#replaces the rgb colorscale with a custom one
	#sets the color explicitly at three intermediate color anchors (511, 660, 1000) 
	#adds a linear gradient between the anchors 
	set color_start [colorinfo num]
	display update off

	for {set i $PointA} {$i < $PointB} {incr i} {

		set deltaPoint [expr $PointB - $PointA]
		set colorList {}
		foreach pa $ColorA pb $ColorB {
			set deltaColor [expr $pb - $pa]

			set color [expr [expr $deltaColor / $deltaPoint] * [expr $i - $PointA] + $pa]
			lappend colorList $color
		}

		color change rgb [expr $i + $color_start] [lindex $colorList 0] [lindex $colorList 1] [lindex $colorList 2]
	}
	display update on
return
}

#
#	Program that sets colorscale to be inline with blobulation colorscheme, creates a gradient 
#
#	Arguments:
# 	PointA (Integer): Starting value used to start i at the desired color num
#	PointB (Integer): Ending value used to end the iteration to 
#	ColorA (List): List of color values, start point that increments up to the end point
# 	ColorB (List): List of color values, end point 
proc colorScale {{pointA 0} {pointB 205} {pointC 410} {pointD 615} {pointE 820} {pointF 1024} {colorA "0.0 0.5 0.5"} {colorB "0.4 1.0 1.0"} {colorC "0.0 0.3 0.6"} {colorD "0.4 0.7 1.0"} {colorE "0.0 0.0 0.6"} {colorF "0.2 0.2 1.0"}} {
	tricolor_scale $pointA $pointB $colorA $colorB
	tricolor_scale $pointB $pointC $colorB $colorC
	tricolor_scale $pointC $pointD $colorC $colorD
	tricolor_scale $pointD $pointE $colorD $colorE
	tricolor_scale $pointE $pointF $colorE $colorF
return
}